"""
HeartInsight — Pipeline Configuration
=======================================
Central path definitions and constants for the data pipeline.
All paths are computed relative to the project root.
"""

import os

# ── Project Root ──
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Data Layer Paths ──
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")
CURATED_DIR = os.path.join(DATA_DIR, "curated")

# ── Source File ──
SOURCE_CSV = os.path.join(DATA_DIR, "heart.csv")

# ── Output Files ──
RAW_COPY = os.path.join(RAW_DIR, "heart_raw.csv")
CLEANED_CSV = os.path.join(CLEANED_DIR, "heart_cleaned.csv")
CURATED_CSV = os.path.join(CURATED_DIR, "heart_curated.csv")
CURATED_PARQUET = os.path.join(CURATED_DIR, "heart_curated.parquet")

# ── Pipeline Metadata ──
PIPELINE_LOG_DIR = os.path.join(PROJECT_ROOT, "pipeline", "logs")
PIPELINE_METADATA_JSON = os.path.join(PIPELINE_LOG_DIR, "last_run.json")

# ── Expected Schema ──
REQUIRED_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
]

EXPECTED_DTYPES = {
    "age": "int",
    "sex": "int",
    "cp": "int",
    "trestbps": "int",
    "chol": "int",
    "fbs": "int",
    "restecg": "int",
    "thalach": "int",
    "exang": "int",
    "oldpeak": "float",
    "slope": "int",
    "ca": "int",
    "thal": "int",
    "target": "int",
}

# ── Valid Category Ranges ──
# These define the expected coded values for categorical columns.
# Values outside these ranges are flagged, NOT silently removed.
VALID_RANGES = {
    "sex": [0, 1],
    "cp": [0, 1, 2, 3],
    "fbs": [0, 1],
    "restecg": [0, 1, 2],
    "exang": [0, 1],
    "slope": [0, 1, 2],
    "ca": [0, 1, 2, 3],
    "thal": [0, 1, 2, 3],
    "target": [0, 1],
}

# ── Physiological Plausibility Bounds ──
# Measurements outside these ranges are flagged as potentially invalid.
# Source: general clinical reference ranges for adult patients.
PLAUSIBILITY_BOUNDS = {
    "age": (1, 120),
    "trestbps": (50, 250),     # Resting BP: extremely low to hypertensive crisis
    "chol": (50, 600),          # Serum cholesterol: very low to extremely high
    "thalach": (50, 250),       # Max heart rate: bradycardia to extreme tachycardia
    "oldpeak": (-5.0, 10.0),    # ST depression: can be slightly negative in some readings
}


def ensure_dirs():
    """Create all pipeline output directories if they don't exist."""
    for d in [RAW_DIR, CLEANED_DIR, CURATED_DIR, PIPELINE_LOG_DIR]:
        os.makedirs(d, exist_ok=True)
