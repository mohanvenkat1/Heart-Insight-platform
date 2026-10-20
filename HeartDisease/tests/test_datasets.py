"""
Tests for Cardiovascular Benchmark Datasets
============================================
Verifies all 6 benchmark datasets and canonical files are present,
accessible, and non-empty.
"""

import os
import pytest
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCHMARKS_DIR = os.path.join(PROJECT_ROOT, "data", "benchmarks")
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")


def test_canonical_cleveland_303():
    """Verify canonical 303-patient Cleveland dataset."""
    p = os.path.join(RAW_DIR, "cleveland_303.csv")
    assert os.path.exists(p)
    df = pd.read_csv(p)
    assert len(df) == 303
    assert len(df.columns) == 14
    assert df.isnull().sum().sum() == 0


@pytest.mark.parametrize("filename,expected_rows,expected_cols", [
    ("heart_attack_cleveland_303.csv", 303, 14),
    ("heart_disease_extended_1025.csv", 1025, 14),
    ("heart_failure_multi_center_918.csv", 918, 12),
    ("heart_statlog_cleveland_hungary_1190.csv", 1190, 12),
    ("heart_failure_clinical_records_299.csv", 299, 13),
    ("heart_attack_risk_factors_9651.csv", 9651, 27),
])
def test_benchmark_datasets_exist_and_valid(filename, expected_rows, expected_cols):
    """Verify each benchmark dataset in data/benchmarks/."""
    p = os.path.join(BENCHMARKS_DIR, filename)
    assert os.path.exists(p), f"Missing benchmark dataset: {p}"
    df = pd.read_csv(p)
    assert len(df) == expected_rows, f"Row mismatch for {filename}: expected {expected_rows}, got {len(df)}"
    assert len(df.columns) == expected_cols, f"Col mismatch for {filename}: expected {expected_cols}, got {len(df.columns)}"


def test_documentation_pdfs_present():
    """Verify documentation PDFs moved to docs/."""
    docs_dir = os.path.join(PROJECT_ROOT, "docs")
    assert os.path.exists(os.path.join(docs_dir, "documentation.pdf"))
    assert os.path.exists(os.path.join(docs_dir, "Heart Disease Prediction - Jupyter Notebook.pdf"))
