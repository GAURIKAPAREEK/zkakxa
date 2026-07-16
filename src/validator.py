import pandas as pd
import logging
from datetime import datetime

from src.cleaning import expand_validation_rules, _null_mask


def apply_validation_rules(df: pd.DataFrame, config: dict) -> tuple:
    """
    Config mein defined rules ko data pe apply karta hai.
    Har row ke liye check karta hai ki koi rule violate to nahi ho rahi.

    Returns: (violations_list, validation_summary)
    """
    rules = expand_validation_rules(df, config)
    violations = []
    treat_empty = config.get("cleaning", {}).get("treat_empty_as_null", True)

    for rule in rules:
        col = rule["column"]

        if col not in df.columns:
            continue

        condition = rule["condition"]
        threshold = rule["value"]

        if condition == "less_than":
            failing_rows = df[df[col] < threshold]
        elif condition == "greater_than":
            failing_rows = df[df[col] > threshold]
        elif condition == "is_null":
            failing_rows = df[df[col].isnull()]
        elif condition == "is_null_or_empty":
            failing_rows = df[_null_mask(df[col], treat_empty)]
        else:
            continue

        for idx in failing_rows.index:
            violations.append({
                "row_index": idx,
                "rule_name": rule["name"],
                "column": col,
                "severity": rule["severity"],
                "actual_value": df.loc[idx, col],
                "detected_at": str(datetime.now())
            })

    # Summary banao
    summary = {
        "total_rows_checked": len(df),
        "total_violations": len(violations),
        "critical_violations": len([v for v in violations if v["severity"] == "CRITICAL"]),
        "warning_violations": len([v for v in violations if v["severity"] == "WARNING"])
    }

    logging.info(f"Validation complete: {summary['total_violations']} violations found "
                 f"({summary['critical_violations']} critical, {summary['warning_violations']} warning)")

    return violations, summary