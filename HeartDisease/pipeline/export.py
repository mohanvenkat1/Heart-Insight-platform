"""
HeartInsight — Export Stage
=============================
Save the cleaned DataFrame to multiple formats:
    - Cleaned CSV  (data/cleaned/)  — human-readable intermediate
    - Curated CSV  (data/curated/)  — analysis-ready with all columns
    - Curated Parquet (data/curated/) — columnar format for DuckDB

Returns:
    dict: Export report with file paths and sizes.
"""

import os
import pandas as pd
from pipeline.config import CLEANED_CSV, CURATED_CSV, CURATED_PARQUET, ensure_dirs


def export(df: pd.DataFrame) -> dict:
    """
    Export the cleaned DataFrame to CSV and Parquet.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned and enriched DataFrame.

    Returns
    -------
    report : dict
        Export metadata (file paths, sizes, row counts).
    """
    ensure_dirs()

    report = {
        "stage": "export",
        "status": "pending",
        "output_rows": len(df),
        "output_columns": len(df.columns),
        "files": [],
    }

    # ── 1. Cleaned CSV ──
    df.to_csv(CLEANED_CSV, index=False)
    cleaned_size = os.path.getsize(CLEANED_CSV)
    report["files"].append({
        "path": CLEANED_CSV,
        "format": "csv",
        "size_bytes": cleaned_size,
        "size_kb": round(cleaned_size / 1024, 1),
    })

    # ── 2. Curated CSV (same data, different location for clarity) ──
    df.to_csv(CURATED_CSV, index=False)
    curated_csv_size = os.path.getsize(CURATED_CSV)
    report["files"].append({
        "path": CURATED_CSV,
        "format": "csv",
        "size_bytes": curated_csv_size,
        "size_kb": round(curated_csv_size / 1024, 1),
    })

    # ── 3. Curated Parquet ──
    df.to_parquet(CURATED_PARQUET, index=False, engine="pyarrow")
    parquet_size = os.path.getsize(CURATED_PARQUET)
    report["files"].append({
        "path": CURATED_PARQUET,
        "format": "parquet",
        "size_bytes": parquet_size,
        "size_kb": round(parquet_size / 1024, 1),
    })

    report["status"] = "success"

    print(f"[EXPORT] [OK] Export complete -- {len(df)} rows to 3 files:")
    for f in report["files"]:
        print(f"[EXPORT]    {f['format'].upper():8s} {f['size_kb']:>8.1f} KB -> {f['path']}")

    return report
