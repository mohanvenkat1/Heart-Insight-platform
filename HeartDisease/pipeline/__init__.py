"""
HeartInsight — Data Pipeline Package
=====================================
Repeatable ETL pipeline for the UCI Heart Disease dataset.

Stages:
    1. ingest   — Load raw CSV, validate schema
    2. validate — Data quality checks (nulls, dupes, ranges, categories)
    3. transform — Clean and enrich the dataset
    4. export   — Save cleaned CSV + curated Parquet
    5. sql_analytics — Run DuckDB analytical queries

Usage:
    python -m pipeline.run_pipeline
"""

__version__ = "1.0.0"
