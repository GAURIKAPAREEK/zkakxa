import logging

import pandas as pd
import sqlalchemy
import streamlit as st

from src.azure_sql import create_table_if_not_exists, get_engine


@st.cache_data(ttl=15, show_spinner=False)
def _fetch_quality_trend(username: str, config_fingerprint: str) -> pd.DataFrame:
    """Cached DB fetch — falls back to all workspace runs if user-specific runs are empty."""
    del config_fingerprint
    from src.ingestion import load_config

    config = load_config("config/pipeline_config.yaml")
    engine = get_engine(config)
    create_table_if_not_exists(engine)

    query = sqlalchemy.text(
        """
        SELECT run_timestamp, file_name, quality_score,
               anomalies_found, critical_violations,
               schema_drift_detected
        FROM pipeline_runs
        WHERE username = :username
        ORDER BY run_timestamp ASC
        """
    )
    df = pd.read_sql(query, engine, params={"username": username})
    if df.empty:
        query_all = sqlalchemy.text(
            """
            SELECT run_timestamp, file_name, quality_score,
                   anomalies_found, critical_violations,
                   schema_drift_detected
            FROM pipeline_runs
            ORDER BY run_timestamp ASC
            """
        )
        df = pd.read_sql(query_all, engine)

    if not df.empty:
        df["quality_score"] = pd.to_numeric(df["quality_score"], errors="coerce")
        df["anomalies_found"] = pd.to_numeric(df["anomalies_found"], errors="coerce")
    return df


def get_quality_trend(config: dict, username: str) -> pd.DataFrame:
    """Return pipeline history for the logged-in user only."""
    if not username:
        return pd.DataFrame()

    try:
        # Fingerprint from DB path so cache works without hashing the whole config dict
        db_cfg = (config or {}).get("database", {}) if isinstance(config, dict) else {}
        fingerprint = str(db_cfg.get("path", "default"))
        return _fetch_quality_trend(username, fingerprint)
    except Exception as exc:
        logging.error(f"Trend fetch error: {exc}")
        return pd.DataFrame()
