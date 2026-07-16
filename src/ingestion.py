import pandas as pd
import os
import yaml
import logging
from datetime import datetime

from src.paths import PROJECT_ROOT, resolve_path

log_dir = resolve_path("logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "pipeline_runs.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def load_config(config_path="config/pipeline_config.yaml"):
    """Config file load karta hai — saari settings yahan se control hoti hain."""
    path = config_path if os.path.isabs(config_path) else resolve_path(config_path)
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_csv_robust(file_path: str) -> pd.DataFrame:
    """Try common encodings so Windows CSV exports don't crash on upload."""
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1", "iso-8859-1"]
    last_error = None
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
    raise ValueError(
        f"Could not read CSV '{os.path.basename(file_path)}'. "
        f"Tried: {', '.join(encodings)}."
    ) from last_error


def load_file(file_path: str) -> tuple:
    ext = file_path.split(".")[-1].lower()
    supported = ["csv", "json", "xlsx"]

    if ext not in supported:
        raise ValueError(f"Format '{ext}' supported nahi hai. Allowed: {supported}")

    start_time = datetime.now()

    if ext == "csv":
        df = load_csv_robust(file_path)
    elif ext == "json":
        df = pd.read_json(file_path)
    elif ext == "xlsx":
        df = pd.read_excel(file_path, engine="openpyxl")

    load_time = (datetime.now() - start_time).total_seconds()

    metadata = {
        "file_name": os.path.basename(file_path),
        "file_format": ext,
        "file_size_kb": round(os.path.getsize(file_path) / 1024, 2),
        "load_time_seconds": load_time,
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "loaded_at": str(start_time)
    }

    logging.info(f"File loaded: {metadata['file_name']} | "
                 f"Rows: {metadata['row_count']} | Cols: {metadata['column_count']}")

    return df, metadata