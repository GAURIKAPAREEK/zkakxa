import os

import pandas as pd

from src.paths import resolve_path


def _null_mask(series: pd.Series, treat_empty_as_null: bool) -> pd.Series:
    mask = series.isnull()
    if treat_empty_as_null:
        as_str = series.astype(str).str.strip()
        mask = mask | as_str.isin(["", "nan", "None", "NaN"])
    return mask


def get_optional_columns(df: pd.DataFrame, config: dict) -> set[str]:
    cleaning = config.get("cleaning", {})
    optional = set(cleaning.get("optional_column_names", []))
    optional_suffixes = cleaning.get("optional_suffixes", [])

    for col in df.columns:
        col_lower = col.lower()
        if any(col_lower.endswith(suffix.lower()) for suffix in optional_suffixes):
            optional.add(col)
    return optional


def get_required_columns(df: pd.DataFrame, config: dict) -> list[str]:
    cleaning = config.get("cleaning", {})
    explicit = cleaning.get("required_column_names", [])
    suffixes = cleaning.get("required_suffixes", ["_id"])
    optional = get_optional_columns(df, config)
    required = set()

    explicit_lower = {name.lower() for name in explicit}
    for col in df.columns:
        if col in optional:
            continue
        col_lower = col.lower()
        if col_lower in explicit_lower:
            required.add(col)
            continue
        if any(col_lower.endswith(suffix.lower()) for suffix in suffixes):
            required.add(col)

    return sorted(required)


def expand_validation_rules(df: pd.DataFrame, config: dict) -> list[dict]:
    """Static rules + dataset-aware null rules so clean output is actually clean."""
    rules = list(config.get("validation_rules", []))
    cleaning = config.get("cleaning", {})
    mode = cleaning.get("mode", "strict")
    treat_empty = cleaning.get("treat_empty_as_null", True)
    condition = "is_null_or_empty" if treat_empty else "is_null"

    covered = {(rule["column"], rule["condition"]) for rule in rules if "column" in rule}

    if mode == "strict":
        target_columns = list(df.columns)
    elif mode == "required_only":
        target_columns = get_required_columns(df, config)
    else:
        return rules

    for col in target_columns:
        key = (col, condition)
        if key in covered:
            continue
        rules.append(
            {
                "name": f"missing_{col}",
                "column": col,
                "condition": condition,
                "value": None,
                "severity": "CRITICAL",
            }
        )
        covered.add(key)

    return rules


def count_null_cells(df: pd.DataFrame, config: dict, required_only: bool = False) -> int:
    treat_empty = config.get("cleaning", {}).get("treat_empty_as_null", True)
    optional = get_optional_columns(df, config) if required_only else set()
    columns = [col for col in df.columns if col not in optional]
    total = 0
    for col in columns:
        total += int(_null_mask(df[col], treat_empty).sum())
    return total


def verify_clean_data(clean_df: pd.DataFrame, config: dict) -> dict:
    treat_empty = config.get("cleaning", {}).get("treat_empty_as_null", True)
    if clean_df.empty:
        return {"rows": 0, "null_rows": 0, "null_cells": 0, "is_fully_clean": True}

    optional = get_optional_columns(clean_df, config)
    check_columns = [col for col in clean_df.columns if col not in optional]
    if not check_columns:
        check_columns = list(clean_df.columns)

    null_mask = pd.DataFrame(
        {col: _null_mask(clean_df[col], treat_empty) for col in check_columns}
    )
    null_rows = int(null_mask.any(axis=1).sum())
    null_cells = int(null_mask.sum().sum())
    return {
        "rows": len(clean_df),
        "null_rows": null_rows,
        "null_cells": null_cells,
        "is_fully_clean": null_cells == 0,
    }


def save_clean_data(clean_df: pd.DataFrame, config: dict, source_filename: str) -> str | None:
    if clean_df.empty:
        return None

    cleaned_path = resolve_path(config["output"]["cleaned_path"])
    os.makedirs(cleaned_path, exist_ok=True)
    output_file = os.path.join(cleaned_path, f"clean_{source_filename}")
    clean_df.to_csv(output_file, index=False)
    return output_file
