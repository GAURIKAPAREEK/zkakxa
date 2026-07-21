import pandas as pd
import numpy as np
from datetime import datetime


def profile_dataframe(df: pd.DataFrame, config: dict) -> dict:
    """
    DataFrame ka complete health profile banata hai:
    - Har column ka data type
    - Null percentage
    - Unique values count
    - Basic statistics (numeric columns ke liye)
    """
    profile = {
        "profiled_at": str(datetime.now()),
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "column_profiles": {}
    }

    null_warn_threshold = config["profiling"]["null_threshold_warning"]
    null_critical_threshold = config["profiling"]["null_threshold_critical"]

    for col in df.columns:
        col_data = df[col]
        null_count = col_data.isnull().sum()
        null_pct = round(null_count / len(df), 4) if len(df) > 0 else 0

        if null_pct >= null_critical_threshold:
            severity = "CRITICAL"
        elif null_pct >= null_warn_threshold:
            severity = "WARNING"
        else:
            severity = "OK"

        col_profile = {
            "data_type": str(col_data.dtype),
            "null_count": int(null_count),
            "null_percentage": null_pct,
            "severity": severity,
            "unique_count": int(col_data.nunique()),
            "is_unique": col_data.nunique() == len(df)
        }

        if pd.api.types.is_numeric_dtype(col_data):
            col_profile.update({
                "min": float(col_data.min()) if not col_data.isnull().all() else None,
                "max": float(col_data.max()) if not col_data.isnull().all() else None,
                "mean": float(col_data.mean()) if not col_data.isnull().all() else None,
                "std": float(col_data.std()) if not col_data.isnull().all() else None
            })

        profile["column_profiles"][col] = col_profile

    profile["overall_quality_score"] = calculate_quality_score(profile)

    return profile


def calculate_quality_score(profile: dict) -> float:
    """
    Har column ki severity dekh ke ek overall score (0-100) banata hai.
    OK = 100, WARNING = 50, CRITICAL = 0 — phir average.
    """
    scores = []
    for col, details in profile["column_profiles"].items():
        if details["severity"] == "OK":
            scores.append(100)
        elif details["severity"] == "WARNING":
            scores.append(50)
        else:
            scores.append(0)

    return round(sum(scores) / len(scores), 2) if scores else 0