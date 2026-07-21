import pandas as pd
import os
import logging
from datetime import datetime

from src.paths import resolve_path


def quarantine_bad_rows(df: pd.DataFrame, violations: list, config: dict) -> tuple:
    """
    CRITICAL violations wali rows ko quarantine mein bhejta hai.
    WARNING violations wali rows clean data mein rehti hain, but flag ho jaati hain.
    
    Returns: (clean_df, quarantined_df)
    """
    # Sirf CRITICAL violations wale row indices nikalo
    critical_row_indices = set(
        v["row_index"] for v in violations if v["severity"] == "CRITICAL"
    )

    if not critical_row_indices:
        # Koi critical issue nahi — sab clean
        return df.copy(), pd.DataFrame()

    # Data split karo — quarantine vs clean
    quarantined_df = df.loc[list(critical_row_indices)].copy()
    clean_df = df.drop(index=list(critical_row_indices)).copy()

    # Quarantine mein reason column add karo — har row ko pata ho kyun yahan hai
    reasons = []
    for idx in quarantined_df.index:
        row_violations = [v for v in violations if v["row_index"] == idx and v["severity"] == "CRITICAL"]
        reason_text = "; ".join([f"{v['rule_name']} (column: {v['column']}, value: {v['actual_value']})" 
                                   for v in row_violations])
        reasons.append(reason_text)

    quarantined_df["quarantine_reason"] = reasons
    quarantined_df["quarantined_at"] = str(datetime.now())

    logging.info(f"Quarantine complete: {len(quarantined_df)} rows quarantined, "
                 f"{len(clean_df)} rows remain clean")

    return clean_df, quarantined_df


def save_quarantine(quarantined_df: pd.DataFrame, config: dict, source_filename: str):
    """Quarantined rows ko CSV mein save karta hai audit ke liye."""
    if quarantined_df.empty:
        return None

    quarantine_path = resolve_path(config["output"]["quarantine_path"])
    os.makedirs(quarantine_path, exist_ok=True)

    output_file = os.path.join(quarantine_path, f"quarantine_{source_filename}")
    quarantined_df.to_csv(output_file, index=False)

    logging.info(f"Quarantine file saved: {output_file}")
    return output_file