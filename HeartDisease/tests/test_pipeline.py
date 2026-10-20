"""
Tests for HeartInsight Data Pipeline
====================================
Validates ingest, quality checks, clinical transformation, Parquet export,
and DuckDB analytics.
"""

import os
import pytest
import pandas as pd
from pipeline.config import (
    SOURCE_CSV, CURATED_CSV, CURATED_PARQUET,
    REQUIRED_COLUMNS, PLAUSIBILITY_BOUNDS
)
from pipeline.ingest import ingest
from pipeline.validate import validate
from pipeline.transform import transform
from pipeline.export import export
from pipeline.sql_analytics import run_analytics
from pipeline.run_pipeline import run_pipeline


def test_source_csv_exists():
    """Verify primary heart.csv exists and is readable."""
    assert os.path.exists(SOURCE_CSV), f"Source CSV missing at {SOURCE_CSV}"
    df = pd.read_csv(SOURCE_CSV)
    assert len(df) > 0
    assert all(col in df.columns for col in REQUIRED_COLUMNS)


def test_ingest_stage():
    """Test ingestion stage loads schema properly."""
    df, report = ingest()
    assert report["status"] == "success"
    assert len(df) == 310
    assert len(df.columns) == 14
    assert report["issues"] == []


def test_validate_stage():
    """Test data validation flags duplicates and calculates quality score."""
    df, _ = ingest()
    report = validate(df)
    assert report["status"] == "success"
    assert report["summary"]["total_duplicate_rows"] == 78
    assert report["summary"]["data_quality_score"] > 95.0


def test_transform_stage():
    """Test transformation drops duplicates and adds 14 derived clinical features."""
    df, _ = ingest()
    df_clean, report = transform(df)
    assert report["status"] == "success"
    assert len(df_clean) == 232  # 310 - 78 duplicates
    assert len(df_clean.columns) == 28
    assert "risk_score" in df_clean.columns
    assert "risk_level" in df_clean.columns
    assert "bp_category" in df_clean.columns
    assert "cholesterol_category" in df_clean.columns


def test_export_stage():
    """Test export generates Cleaned CSV, Curated CSV, and Curated Parquet."""
    df, _ = ingest()
    df_clean, _ = transform(df)
    report = export(df_clean)
    assert report["status"] == "success"
    assert len(report["files"]) == 3
    assert os.path.exists(CURATED_CSV)
    assert os.path.exists(CURATED_PARQUET)


def test_sql_analytics_duckdb():
    """Test DuckDB analytical queries execute on Parquet with zero errors."""
    report = run_analytics()
    assert report["status"] == "success"
    assert len(report["queries"]) == 8
    for q in report["queries"]:
        assert q["rows_returned"] > 0
        assert q["time_ms"] >= 0


def test_full_pipeline_orchestration_reconciles():
    """Test end-to-end pipeline run and row reconciliation."""
    meta = run_pipeline()
    assert meta["status"] == "success"
    rec = meta["reconciliation"]
    assert rec["reconciles"] is True
    assert rec["input_rows"] - rec["rows_dropped_duplicates"] == rec["output_rows"]
