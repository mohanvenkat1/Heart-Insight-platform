"""
HeartInsight — Ingestion Stage
================================
Load the raw CSV, validate that required columns exist and have expected
data types.  Preserve the original file untouched by copying it to the
raw/ layer.

Returns:
    tuple: (DataFrame, ingestion_report dict)
"""

import os
import shutil
import pandas as pd
from pipeline.config import (
    SOURCE_CSV, RAW_COPY, REQUIRED_COLUMNS, EXPECTED_DTYPES, ensure_dirs
)


def ingest(source_path: str | None = None) -> tuple[pd.DataFrame, dict]:
    """
    Load the source CSV and validate its schema.

    Parameters
    ----------
    source_path : str, optional
        Override path to the source CSV. Defaults to config.SOURCE_CSV.

    Returns
    -------
    df : pd.DataFrame
        Raw data loaded into memory.
    report : dict
        Ingestion metadata (row count, column count, issues found).

    Raises
    ------
    FileNotFoundError
        If the source CSV does not exist.
    ValueError
        If required columns are missing.
    """
    source = source_path or SOURCE_CSV
    report = {
        "stage": "ingest",
        "source_path": source,
        "status": "pending",
        "issues": [],
    }

    # ── 1. Check file exists ──
    if not os.path.exists(source):
        report["status"] = "error"
        report["issues"].append(f"Source file not found: {source}")
        raise FileNotFoundError(f"Source CSV not found: {source}")

    # ── 2. Load CSV ──
    df = pd.read_csv(source)
    report["input_rows"] = len(df)
    report["input_columns"] = len(df.columns)
    report["columns_found"] = list(df.columns)

    # ── 3. Validate required columns ──
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        report["status"] = "error"
        report["issues"].append(f"Missing required columns: {missing_cols}")
        raise ValueError(f"Missing required columns: {missing_cols}")

    extra_cols = [c for c in df.columns if c not in REQUIRED_COLUMNS]
    if extra_cols:
        report["issues"].append(f"Extra columns found (will be kept): {extra_cols}")

    # ── 4. Coerce types ──
    type_issues = []
    for col, expected in EXPECTED_DTYPES.items():
        if col not in df.columns:
            continue
        # Replace '?' with NaN (common in UCI datasets)
        df[col] = df[col].replace("?", pd.NA)
        if expected == "float":
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Check if any non-integer values exist (after coercion)
            non_null = df[col].dropna()
            if len(non_null) > 0 and not (non_null == non_null.astype(int)).all():
                type_issues.append(f"Column '{col}' has non-integer values")

    if type_issues:
        report["issues"].extend(type_issues)

    # ── 5. Preserve raw copy ──
    ensure_dirs()
    shutil.copy2(source, RAW_COPY)
    report["raw_copy_path"] = RAW_COPY

    report["status"] = "success"
    print(f"[INGEST] [OK] Loaded {len(df)} rows x {len(df.columns)} columns from {source}")
    if report["issues"]:
        for issue in report["issues"]:
            print(f"[INGEST] [WARN] {issue}")

    return df, report
