import pandas as pd
import numpy as np
import logging
from datetime import datetime


def detect_statistical_anomalies(df: pd.DataFrame, profile: dict, config: dict) -> list:
    """
    Numeric columns mein statistical outliers dhundta hai using Z-score method.
    Z-score batata hai ki ek value, average se kitni standard deviations door hai.
    Agar |Z-score| > 3, to wo value 'unusual' maani jaati hai.
    """
    anomalies = []
    z_threshold = config.get("anomaly_detection", {}).get("z_score_threshold", 3)

    for col, col_profile in profile["column_profiles"].items():
        # Sirf numeric columns pe ye check chalega
        if "mean" not in col_profile or col_profile["mean"] is None:
            continue

        mean = col_profile["mean"]
        std = col_profile["std"]

        # Agar std deviation 0 hai (sab values same hain), skip karo
        if std is None or std == 0:
            continue

        col_data = df[col].dropna()

        for idx, value in col_data.items():
            z_score = (value - mean) / std

            if abs(z_score) > z_threshold:
                anomalies.append({
                    "row_index": idx,
                    "column": col,
                    "value": float(value),
                    "z_score": round(float(z_score), 2),
                    "column_mean": round(mean, 2),
                    "column_std": round(std, 2),
                    "detected_at": str(datetime.now())
                })

    logging.info(f"Anomaly detection complete: {len(anomalies)} anomalies found")
    return anomalies


def detect_volume_anomaly(current_row_count: int, previous_row_count: int, config: dict) -> dict:
    """
    Compare karta hai ki aaj ka data pichli baar se kitna alag hai size mein.
    Agar achanak bahut zyada rows kam/zyada ho jayein, ye suspicious hai.
    """
    if previous_row_count == 0:
        return {"is_anomaly": False, "reason": "No previous data to compare"}

    change_pct = ((current_row_count - previous_row_count) / previous_row_count) * 100
    threshold = config.get("anomaly_detection", {}).get("volume_change_threshold_pct", 50)

    is_anomaly = abs(change_pct) > threshold

    return {
        "is_anomaly": is_anomaly,
        "current_rows": current_row_count,
        "previous_rows": previous_row_count,
        "change_percentage": round(change_pct, 2),
        "reason": f"Row count changed by {round(change_pct, 2)}%" if is_anomaly else "Normal variation"
    }