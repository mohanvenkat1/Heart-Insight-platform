"""
HeartInsight — Pipeline Orchestrator
======================================
Runs the full ETL pipeline in sequence:
    1. Ingest  → load CSV, validate schema
    2. Validate → check data quality (report only)
    3. Transform → clean and enrich
    4. Export   → save CSV + Parquet
    5. Analytics → run DuckDB queries

Records execution metadata (timing, row counts, status) to a JSON log.
Supports safe reruns — output files are overwritten, not appended.

Usage:
    python -m pipeline.run_pipeline
"""

import json
import time
import traceback
from datetime import datetime, timezone

from pipeline.config import PIPELINE_METADATA_JSON, ensure_dirs
from pipeline.ingest import ingest
from pipeline.validate import validate
from pipeline.transform import transform
from pipeline.export import export
from pipeline.sql_analytics import run_analytics


def run_pipeline(source_path: str | None = None) -> dict:
    """
    Execute the full pipeline and return the combined metadata.

    Parameters
    ----------
    source_path : str, optional
        Override path to the source CSV.

    Returns
    -------
    metadata : dict
        Combined report from all stages.
    """
    ensure_dirs()

    metadata = {
        "pipeline_version": "1.0.0",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "running",
        "stages": {},
        "errors": [],
    }

    overall_start = time.perf_counter()

    print("\n" + "=" * 65)
    print("  [HeartInsight] -- Data Pipeline")
    print("=" * 65 + "\n")

    try:
        # ── Stage 1: Ingest ──
        stage_start = time.perf_counter()
        df_raw, ingest_report = ingest(source_path)
        ingest_report["duration_ms"] = round((time.perf_counter() - stage_start) * 1000, 1)
        metadata["stages"]["ingest"] = ingest_report
        print()

        # ── Stage 2: Validate ──
        stage_start = time.perf_counter()
        validate_report = validate(df_raw)
        validate_report["duration_ms"] = round((time.perf_counter() - stage_start) * 1000, 1)
        metadata["stages"]["validate"] = validate_report
        print()

        # ── Stage 3: Transform ──
        stage_start = time.perf_counter()
        df_clean, transform_report = transform(df_raw)
        transform_report["duration_ms"] = round((time.perf_counter() - stage_start) * 1000, 1)
        metadata["stages"]["transform"] = transform_report
        print()

        # ── Stage 4: Export ──
        stage_start = time.perf_counter()
        export_report = export(df_clean)
        export_report["duration_ms"] = round((time.perf_counter() - stage_start) * 1000, 1)
        metadata["stages"]["export"] = export_report
        print()

        # ── Stage 5: Analytics ──
        stage_start = time.perf_counter()
        analytics_report = run_analytics()
        analytics_report["duration_ms"] = round((time.perf_counter() - stage_start) * 1000, 1)
        metadata["stages"]["analytics"] = analytics_report
        print()

        metadata["status"] = "success"

    except Exception as e:
        metadata["status"] = "error"
        metadata["errors"].append({
            "error": str(e),
            "traceback": traceback.format_exc(),
        })
        print(f"\n[PIPELINE] [ERROR] Pipeline failed: {e}")

    # -- Record Timing --
    total_ms = round((time.perf_counter() - overall_start) * 1000, 1)
    metadata["finished_at"] = datetime.now(timezone.utc).isoformat()
    metadata["total_duration_ms"] = total_ms

    # -- Reconciliation Summary --
    if metadata["status"] == "success":
        ingest_r = metadata["stages"]["ingest"]
        transform_r = metadata["stages"]["transform"]
        export_r = metadata["stages"]["export"]

        metadata["reconciliation"] = {
            "input_rows": ingest_r["input_rows"],
            "rows_dropped_nulls": transform_r["rows_dropped_nulls"],
            "rows_dropped_duplicates": transform_r["rows_dropped_duplicates"],
            "output_rows": export_r["output_rows"],
            "reconciles": (
                ingest_r["input_rows"]
                - transform_r["rows_dropped_nulls"]
                - transform_r["rows_dropped_duplicates"]
                == export_r["output_rows"]
            ),
        }

    # -- Save Metadata --
    with open(PIPELINE_METADATA_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, default=str)

    # -- Final Summary --
    print("=" * 65)
    print("  PIPELINE SUMMARY")
    print("=" * 65)
    print(f"  Status:       {metadata['status'].upper()}")
    print(f"  Total time:   {total_ms:.1f} ms")

    if metadata["status"] == "success":
        rec = metadata["reconciliation"]
        print(f"  Input rows:   {rec['input_rows']}")
        print(f"  Dropped:      {rec['rows_dropped_nulls']} nulls + "
              f"{rec['rows_dropped_duplicates']} dupes")
        print(f"  Output rows:  {rec['output_rows']}")
        print(f"  Reconciles:   {'[OK] Yes' if rec['reconciles'] else '[FAIL] No'}")

    print(f"  Metadata:     {PIPELINE_METADATA_JSON}")
    print("=" * 65 + "\n")

    return metadata


if __name__ == "__main__":
    run_pipeline()
