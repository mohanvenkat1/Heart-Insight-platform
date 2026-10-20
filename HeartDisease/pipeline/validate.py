"""
HeartInsight — Validation Stage
=================================
Perform data quality checks on the ingested DataFrame.
Reports issues but does NOT drop or modify data — that is the
transform stage's responsibility.

Checks performed:
    1. Missing values per column
    2. Duplicate rows
    3. Out-of-range categorical values
    4. Physiologically implausible measurements
    5. Row-level summary

Returns:
    dict: Comprehensive validation report.
"""

import pandas as pd
from pipeline.config import VALID_RANGES, PLAUSIBILITY_BOUNDS, REQUIRED_COLUMNS


def validate(df: pd.DataFrame) -> dict:
    """
    Run all data quality checks on the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Ingested (raw) data.

    Returns
    -------
    report : dict
        Validation results including counts and row indices for each issue.
    """
    report = {
        "stage": "validate",
        "status": "pending",
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_values": {},
        "duplicate_rows": {},
        "invalid_categories": {},
        "implausible_values": {},
        "summary": {},
    }

    # ── 1. Missing Values ──
    missing = {}
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            continue
        null_count = int(df[col].isna().sum())
        if null_count > 0:
            null_indices = df[df[col].isna()].index.tolist()
            missing[col] = {
                "count": null_count,
                "percentage": round(null_count / len(df) * 100, 2),
                "row_indices": null_indices[:20],  # Cap at 20 for readability
            }
    report["missing_values"] = missing
    total_missing = sum(v["count"] for v in missing.values())

    # ── 2. Duplicate Rows ──
    dupe_mask = df.duplicated(keep="first")
    dupe_count = int(dupe_mask.sum())
    dupe_indices = df[dupe_mask].index.tolist()
    report["duplicate_rows"] = {
        "count": dupe_count,
        "percentage": round(dupe_count / len(df) * 100, 2),
        "row_indices": dupe_indices[:20],
    }

    # ── 3. Invalid Category Values ──
    invalid_cats = {}
    for col, valid_values in VALID_RANGES.items():
        if col not in df.columns:
            continue
        non_null = df[col].dropna()
        invalid_mask = ~non_null.isin(valid_values)
        invalid_count = int(invalid_mask.sum())
        if invalid_count > 0:
            invalid_vals = non_null[invalid_mask].unique().tolist()
            invalid_cats[col] = {
                "count": invalid_count,
                "invalid_values_found": invalid_vals,
                "expected_values": valid_values,
                "row_indices": non_null[invalid_mask].index.tolist()[:20],
            }
    report["invalid_categories"] = invalid_cats

    # ── 4. Implausible Measurements ──
    implausible = {}
    for col, (low, high) in PLAUSIBILITY_BOUNDS.items():
        if col not in df.columns:
            continue
        non_null = df[col].dropna()
        out_mask = (non_null < low) | (non_null > high)
        out_count = int(out_mask.sum())
        if out_count > 0:
            out_vals = non_null[out_mask].unique().tolist()
            implausible[col] = {
                "count": out_count,
                "out_of_range_values": sorted(out_vals)[:20],
                "expected_range": f"[{low}, {high}]",
                "row_indices": non_null[out_mask].index.tolist()[:20],
            }
    report["implausible_values"] = implausible

    # ── 5. Summary ──
    total_issues = (
        total_missing
        + dupe_count
        + sum(v["count"] for v in invalid_cats.values())
        + sum(v["count"] for v in implausible.values())
    )
    report["summary"] = {
        "total_missing_cells": total_missing,
        "total_duplicate_rows": dupe_count,
        "total_invalid_categories": sum(v["count"] for v in invalid_cats.values()),
        "total_implausible_values": sum(v["count"] for v in implausible.values()),
        "total_issues": total_issues,
        "data_quality_score": round(
            max(0, (1 - total_issues / max(1, len(df) * len(REQUIRED_COLUMNS)))) * 100, 1
        ),
    }

    report["status"] = "success"

    # -- Print Summary --
    print(f"[VALIDATE] [OK] Validation complete -- {len(df)} rows checked")
    print(f"[VALIDATE]    Missing cells:        {total_missing}")
    print(f"[VALIDATE]    Duplicate rows:        {dupe_count}")
    print(f"[VALIDATE]    Invalid categories:     {sum(v['count'] for v in invalid_cats.values())}")
    print(f"[VALIDATE]    Implausible values:     {sum(v['count'] for v in implausible.values())}")
    print(f"[VALIDATE]    Quality score:          {report['summary']['data_quality_score']}%")

    return report
