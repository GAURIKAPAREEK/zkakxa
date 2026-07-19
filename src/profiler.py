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


def calculate_quality_score(profile: dict, quarantine_rate: float | None = None) -> float:
    """
    Har column ki severity dekh ke ek column-level score (0-100) banata hai.
    OK = 100, WARNING = 50, CRITICAL = 0 — phir average.

    Agar quarantine_rate diya gaya hai (rows quarantined / total rows), to us
    row-level signal ko bhi blend kiya jaata hai — sirf per-column null % dekhna
    kaafi nahi hai, kyunki alag-alag columns ke chhote-chhote null counts bhi
    row-wise combine ho ke bahut saari rows quarantine karwa sakte hain, jabki
    har column individually threshold ke neeche rehta hai.
    """
    scores = []
    for col, details in profile["column_profiles"].items():
        if details["severity"] == "OK":
            scores.append(100)
        elif details["severity"] == "WARNING":
            scores.append(50)
        else:
            scores.append(0)

    column_score = round(sum(scores) / len(scores), 2) if scores else 0
    if quarantine_rate is None:
        return column_score

    row_score = round((1 - quarantine_rate) * 100, 2)
    # Row-level quarantine rate is weighted higher (60%) since it reflects
    # rows that actually failed hard validation rules — a more direct signal
    # of usable data quality than null-density alone (40%).
    return round((0.4 * column_score) + (0.6 * row_score), 2)


def apply_quarantine_penalty(profile: dict, quarantined_rows: int, total_rows: int) -> dict:
    """
    Quarantine result pata chalne ke baad profile['overall_quality_score'] ko
    update karta hai taaki score sirf column nulls hi nahi, actual quarantine
    rate bhi reflect kare. Original column-only score 'column_quality_score'
    ke naam se preserve rehta hai for reference.
    """
    quarantine_rate = (quarantined_rows / total_rows) if total_rows else 0
    profile["column_quality_score"] = profile.get("overall_quality_score", 0)
    profile["quarantine_rate"] = round(quarantine_rate * 100, 2)
    profile["overall_quality_score"] = calculate_quality_score(profile, quarantine_rate=quarantine_rate)
    return profile
