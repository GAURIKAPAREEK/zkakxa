import os
import sqlalchemy
import pandas as pd
import logging
from datetime import datetime

from src.paths import resolve_path


def get_engine(config: dict):
    db_path = resolve_path(config["database"]["path"])
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db_url = "sqlite:///" + db_path.replace("\\", "/")
    return sqlalchemy.create_engine(db_url)


def _migrate_username_column(conn) -> None:
    rows = conn.execute(sqlalchemy.text("PRAGMA table_info(pipeline_runs)")).fetchall()
    columns = {row[1] for row in rows}
    if "username" not in columns:
        conn.execute(sqlalchemy.text("ALTER TABLE pipeline_runs ADD COLUMN username TEXT"))
        conn.commit()
        logging.info("Added username column to pipeline_runs")


def create_table_if_not_exists(engine):
    create_query = """
    CREATE TABLE IF NOT EXISTS pipeline_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        file_name TEXT,
        file_format TEXT,
        row_count INTEGER,
        column_count INTEGER,
        quality_score REAL,
        critical_violations INTEGER,
        warning_violations INTEGER,
        anomalies_found INTEGER,
        schema_drift_detected INTEGER,
        run_timestamp TEXT
    )
    """
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text(create_query))
        conn.commit()
        _migrate_username_column(conn)
    logging.info("Pipeline runs table ready")


def save_pipeline_run(
    metadata: dict,
    profile: dict,
    validation_summary: dict,
    anomalies: list,
    drift_result: dict,
    config: dict,
    username: str,
):
    engine = get_engine(config)
    create_table_if_not_exists(engine)

    run_data = {
        "username": username,
        "file_name": metadata["file_name"],
        "file_format": metadata["file_format"],
        "row_count": metadata["row_count"],
        "column_count": metadata["column_count"],
        "quality_score": profile["overall_quality_score"],
        "critical_violations": validation_summary["critical_violations"],
        "warning_violations": validation_summary["warning_violations"],
        "anomalies_found": len(anomalies),
        "schema_drift_detected": int(drift_result.get("drift_detected", False)),
        "run_timestamp": str(datetime.now())
    }

    df = pd.DataFrame([run_data])
    df.to_sql("pipeline_runs", engine, if_exists="append", index=False)

    try:
        from src.quality_trend import _fetch_quality_trend

        _fetch_quality_trend.clear()
    except Exception:
        pass

    logging.info(f"Pipeline run saved: {metadata['file_name']}")
    return run_data
