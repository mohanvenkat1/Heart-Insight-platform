"""
HeartInsight — Transform Stage
================================
Clean and enrich the validated DataFrame.

Cleaning strategy (documented):
    - Rows with ANY null in the 14 required columns are DROPPED.
      Justification: The dataset is small (310 rows) and imputation
      of clinical measurements (e.g., cholesterol, thalassemia type)
      would introduce artificial values without clinical justification.
      Dropped rows are counted and reported.
    - Exact duplicate rows are DROPPED (keeping first occurrence).
      Justification: Duplicate clinical records indicate data entry
      errors, not distinct patients.

Enrichment (carried over from the original prepare_data.py):
    - Human-readable labels for coded columns
    - Derived categories (age_group, cholesterol_category, bp_category, hr_category)
    - Composite risk score (heuristic — NOT clinically validated)

Returns:
    tuple: (cleaned DataFrame, transform report dict)
"""

import pandas as pd
from pipeline.config import REQUIRED_COLUMNS


def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Clean and enrich the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Ingested data (may contain nulls, dupes).

    Returns
    -------
    df_clean : pd.DataFrame
        Cleaned and enriched DataFrame.
    report : dict
        Transform metadata (rows dropped, columns added).
    """
    report = {
        "stage": "transform",
        "status": "pending",
        "input_rows": len(df),
        "issues": [],
    }

    # ── Work on a copy to avoid mutating the input ──
    df_clean = df.copy()

    # ──────────────────────────────────────────────────
    # 1. Drop rows with missing values in required columns
    # ──────────────────────────────────────────────────
    # Strategy: drop rows where ANY of the 14 core columns is null.
    # Justification documented in module docstring above.
    available_required = [c for c in REQUIRED_COLUMNS if c in df_clean.columns]
    null_mask = df_clean[available_required].isna().any(axis=1)
    rows_with_nulls = int(null_mask.sum())

    if rows_with_nulls > 0:
        dropped_null_indices = df_clean[null_mask].index.tolist()
        report["rows_dropped_nulls"] = rows_with_nulls
        report["dropped_null_indices"] = dropped_null_indices[:50]
        df_clean = df_clean[~null_mask].copy()
    else:
        report["rows_dropped_nulls"] = 0

    # ──────────────────────────────────────────────────
    # 2. Drop duplicate rows
    # ──────────────────────────────────────────────────
    dupe_mask = df_clean.duplicated(keep="first")
    rows_dupes = int(dupe_mask.sum())
    if rows_dupes > 0:
        dropped_dupe_indices = df_clean[dupe_mask].index.tolist()
        report["rows_dropped_duplicates"] = rows_dupes
        report["dropped_dupe_indices"] = dropped_dupe_indices[:50]
        df_clean = df_clean.drop_duplicates(keep="first").copy()
    else:
        report["rows_dropped_duplicates"] = 0

    # Reset index after drops
    df_clean = df_clean.reset_index(drop=True)
    report["rows_after_cleaning"] = len(df_clean)

    # ──────────────────────────────────────────────────
    # 3. Map coded values to readable labels
    # ──────────────────────────────────────────────────
    df_clean["sex_label"] = df_clean["sex"].map({0: "Female", 1: "Male"})

    df_clean["cp_label"] = df_clean["cp"].map({
        0: "Typical Angina",
        1: "Atypical Angina",
        2: "Non-anginal Pain",
        3: "Asymptomatic",
    })

    df_clean["fbs_label"] = df_clean["fbs"].map({
        0: "≤120 mg/dl (Normal)",
        1: ">120 mg/dl (High)",
    })

    df_clean["restecg_label"] = df_clean["restecg"].map({
        0: "Normal",
        1: "ST-T Abnormality",
        2: "LV Hypertrophy",
    })

    df_clean["exang_label"] = df_clean["exang"].map({0: "No", 1: "Yes"})

    df_clean["slope_label"] = df_clean["slope"].map({
        0: "Upsloping",
        1: "Flat",
        2: "Downsloping",
    })

    # Thalassemia mapping — NOTE: coding varies between dataset versions.
    # This mapping follows the Kaggle/processed Cleveland convention:
    #   0 = Normal, 1 = Fixed Defect, 2 = Reversible Defect, 3 = Thalassemia
    # Some sources use 1/2/3/7 coding. We document this choice explicitly.
    df_clean["thal_label"] = df_clean["thal"].map({
        0: "Normal",
        1: "Fixed Defect",
        2: "Reversible Defect",
        3: "Thalassemia",
    })

    df_clean["diagnosis"] = df_clean["target"].map({
        0: "No Disease",
        1: "Heart Disease",
    })

    # ──────────────────────────────────────────────────
    # 4. Derived categories
    # ──────────────────────────────────────────────────

    # Age Group (10-year bins)
    def _age_group(age):
        if age < 30:
            return "20-29"
        elif age < 40:
            return "30-39"
        elif age < 50:
            return "40-49"
        elif age < 60:
            return "50-59"
        elif age < 70:
            return "60-69"
        else:
            return "70+"

    df_clean["age_group"] = df_clean["age"].apply(_age_group)

    # Cholesterol Category (AHA/NCEP ATP III guidelines)
    def _chol_category(chol):
        if chol < 200:
            return "Desirable"
        elif chol < 240:
            return "Borderline High"
        else:
            return "High"

    df_clean["cholesterol_category"] = df_clean["chol"].apply(_chol_category)

    # Blood Pressure Category (AHA 2017 guidelines)
    def _bp_category(bp):
        if bp < 120:
            return "Normal"
        elif bp < 130:
            return "Elevated"
        elif bp < 140:
            return "High Stage 1"
        else:
            return "High Stage 2"

    df_clean["bp_category"] = df_clean["trestbps"].apply(_bp_category)

    # Heart Rate Category
    def _hr_category(hr):
        if hr < 100:
            return "Low"
        elif hr < 150:
            return "Moderate"
        else:
            return "High"

    df_clean["hr_category"] = df_clean["thalach"].apply(_hr_category)

    # ──────────────────────────────────────────────────
    # 5. Composite Risk Score (HEURISTIC — NOT CLINICALLY VALIDATED)
    # ──────────────────────────────────────────────────
    # This is a simple point-based score for educational demonstration.
    # It is NOT a substitute for validated clinical risk models such as
    # the Framingham Risk Score or ASCVD Pooled Cohort Equations.
    def _risk_score(row):
        score = 0
        if row["age"] >= 55:
            score += 2
        elif row["age"] >= 45:
            score += 1
        if row["chol"] >= 240:
            score += 2
        elif row["chol"] >= 200:
            score += 1
        if row["trestbps"] >= 140:
            score += 2
        elif row["trestbps"] >= 130:
            score += 1
        if row["exang"] == 1:
            score += 2
        if row["oldpeak"] >= 2:
            score += 2
        elif row["oldpeak"] >= 1:
            score += 1
        if row["fbs"] == 1:
            score += 1
        score += int(row["ca"])
        return score

    df_clean["risk_score"] = df_clean.apply(_risk_score, axis=1)

    def _risk_level(score):
        if score <= 2:
            return "Low Risk"
        elif score <= 5:
            return "Moderate Risk"
        elif score <= 8:
            return "High Risk"
        else:
            return "Very High Risk"

    df_clean["risk_level"] = df_clean["risk_score"].apply(_risk_level)

    # ── Report ──
    new_columns = [c for c in df_clean.columns if c not in REQUIRED_COLUMNS]
    report["columns_added"] = new_columns
    report["output_rows"] = len(df_clean)
    report["output_columns"] = len(df_clean.columns)
    report["status"] = "success"

    total_dropped = report["rows_dropped_nulls"] + report["rows_dropped_duplicates"]
    print(f"[TRANSFORM] [OK] Transform complete")
    print(f"[TRANSFORM]    Input:   {report['input_rows']} rows")
    print(f"[TRANSFORM]    Dropped: {total_dropped} rows "
          f"({report['rows_dropped_nulls']} nulls, "
          f"{report['rows_dropped_duplicates']} duplicates)")
    print(f"[TRANSFORM]    Output:  {report['output_rows']} rows x "
          f"{report['output_columns']} columns")
    print(f"[TRANSFORM]    Added:   {len(new_columns)} derived columns")

    return df_clean, report
