import json
import os
import logging
from datetime import datetime

from src.paths import resolve_path


def _snapshot_key(username: str, source_filename: str) -> str:
    safe_user = "".join(c if c.isalnum() or c in "_-" else "_" for c in username)
    return f"{safe_user}__{source_filename}"


def _snapshot_path(username: str, source_filename: str) -> str:
    snapshot_dir = resolve_path("logs/schema_snapshots")
    os.makedirs(snapshot_dir, exist_ok=True)
    return os.path.join(snapshot_dir, f"{_snapshot_key(username, source_filename)}_schema.json")


def save_schema_snapshot(
    df_columns: list,
    df_dtypes: dict,
    config: dict,
    source_filename: str,
    username: str,
):
    snapshot = {
        "username": username,
        "source_filename": source_filename,
        "columns": df_columns,
        "dtypes": df_dtypes,
        "saved_at": str(datetime.now()),
    }

    snapshot_path = _snapshot_path(username, source_filename)
    with open(snapshot_path, "w") as f:
        json.dump(snapshot, f, indent=2)

    return snapshot_path


def detect_schema_drift(
    df_columns: list,
    df_dtypes: dict,
    source_filename: str,
    username: str,
) -> dict:
    snapshot_path = _snapshot_path(username, source_filename)

    # Agar pehli baar ye file aayi hai, koi previous schema nahi hai
    if not os.path.exists(snapshot_path):
        return {
            "drift_detected": False,
            "is_first_run": True,
            "message": "No previous schema found — this is the baseline run."
        }

    with open(snapshot_path, "r") as f:
        old_snapshot = json.load(f)

    old_columns = set(old_snapshot["columns"])
    new_columns = set(df_columns)

    added_columns = list(new_columns - old_columns)
    removed_columns = list(old_columns - new_columns)

    # Type changes check karo un columns ke liye jo dono mein common hain
    type_changes = []
    common_columns = old_columns & new_columns
    for col in common_columns:
        old_type = old_snapshot["dtypes"].get(col)
        new_type = df_dtypes.get(col)
        if old_type != new_type:
            type_changes.append({
                "column": col,
                "old_type": old_type,
                "new_type": new_type
            })

    drift_detected = bool(added_columns or removed_columns or type_changes)

    result = {
        "drift_detected": drift_detected,
        "is_first_run": False,
        "added_columns": added_columns,
        "removed_columns": removed_columns,
        "type_changes": type_changes,
        "checked_at": str(datetime.now())
    }

    if drift_detected:
        logging.warning(f"SCHEMA DRIFT DETECTED for {source_filename}: {result}")
    else:
        logging.info(f"No schema drift detected for {source_filename}")

    return result