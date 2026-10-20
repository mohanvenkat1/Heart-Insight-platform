"""
Heart Disease Analysis - Data Preparation
==========================================
This script cleans and transforms the raw UCI Heart Disease dataset
for use in Tableau visualizations.

Transformations:
- Handle missing/invalid values
- Map coded values to readable labels
- Create derived columns (age_group, cholesterol_category, bp_category, risk_score)
- Export cleaned data as heart_cleaned.csv

Usage:
    python data_preparation/prepare_data.py
"""

import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, "data", "heart.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "heart_cleaned.csv")


def prepare_data():
    """Clean, transform, and enrich the heart disease dataset."""

    # ──────────────────────────────────────────────
    # 1. Load the raw dataset
    # ──────────────────────────────────────────────
    if not os.path.exists(INPUT_CSV):
        print(f"[ERROR] Input CSV not found: {INPUT_CSV}")
        sys.exit(1)

    df = pd.read_csv(INPUT_CSV)
    print(f"[INFO] Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"[INFO] Columns: {list(df.columns)}")

    # ──────────────────────────────────────────────
    # 2. Handle missing values
    # ──────────────────────────────────────────────
    # Replace '?' with NaN and drop rows with missing values
    df = df.replace("?", pd.NA)

    # Convert numeric columns to proper types
    numeric_cols = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
                    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_before = df.isnull().sum().sum()
    df = df.dropna()
    print(f"[INFO] Removed {missing_before} missing values. Remaining: {df.shape[0]} rows")

    # Remove duplicates
    dupes = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"[INFO] Removed {dupes} duplicate rows. Remaining: {df.shape[0]} rows")

    # ──────────────────────────────────────────────
    # 3. Map coded values to readable labels
    # ──────────────────────────────────────────────

    # Sex
    df["sex_label"] = df["sex"].map({0: "Female", 1: "Male"})

    # Chest Pain Type
    df["cp_label"] = df["cp"].map({
        0: "Typical Angina",
        1: "Atypical Angina",
        2: "Non-anginal Pain",
        3: "Asymptomatic"
    })

    # Fasting Blood Sugar
    df["fbs_label"] = df["fbs"].map({
        0: "≤120 mg/dl (Normal)",
        1: ">120 mg/dl (High)"
    })

    # Resting ECG
    df["restecg_label"] = df["restecg"].map({
        0: "Normal",
        1: "ST-T Abnormality",
        2: "LV Hypertrophy"
    })

    # Exercise Induced Angina
    df["exang_label"] = df["exang"].map({
        0: "No",
        1: "Yes"
    })

    # Slope of ST Segment
    df["slope_label"] = df["slope"].map({
        0: "Upsloping",
        1: "Flat",
        2: "Downsloping"
    })

    # Thalassemia
    df["thal_label"] = df["thal"].map({
        0: "Normal",
        1: "Fixed Defect",
        2: "Reversible Defect",
        3: "Thalassemia"
    })

    # Target (Disease)
    df["diagnosis"] = df["target"].map({
        0: "No Disease",
        1: "Heart Disease"
    })

    # ──────────────────────────────────────────────
    # 4. Create derived columns
    # ──────────────────────────────────────────────

    # Age Group
    def age_group(age):
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

    df["age_group"] = df["age"].apply(age_group)

    # Cholesterol Category (based on medical guidelines)
    def chol_category(chol):
        if chol < 200:
            return "Desirable"
        elif chol < 240:
            return "Borderline High"
        else:
            return "High"

    df["cholesterol_category"] = df["chol"].apply(chol_category)

    # Blood Pressure Category (based on AHA guidelines)
    def bp_category(bp):
        if bp < 120:
            return "Normal"
        elif bp < 130:
            return "Elevated"
        elif bp < 140:
            return "High Stage 1"
        else:
            return "High Stage 2"

    df["bp_category"] = df["trestbps"].apply(bp_category)

    # Max Heart Rate Category
    def hr_category(hr):
        if hr < 100:
            return "Low"
        elif hr < 150:
            return "Moderate"
        else:
            return "High"

    df["hr_category"] = df["thalach"].apply(hr_category)

    # Risk Score (composite score based on key indicators)
    def calculate_risk_score(row):
        score = 0

        # Age factor
        if row["age"] >= 55:
            score += 2
        elif row["age"] >= 45:
            score += 1

        # Cholesterol factor
        if row["chol"] >= 240:
            score += 2
        elif row["chol"] >= 200:
            score += 1

        # Blood Pressure factor
        if row["trestbps"] >= 140:
            score += 2
        elif row["trestbps"] >= 130:
            score += 1

        # Exercise angina
        if row["exang"] == 1:
            score += 2

        # ST depression
        if row["oldpeak"] >= 2:
            score += 2
        elif row["oldpeak"] >= 1:
            score += 1

        # Fasting blood sugar
        if row["fbs"] == 1:
            score += 1

        # Major vessels
        score += int(row["ca"])

        return score

    df["risk_score"] = df.apply(calculate_risk_score, axis=1)

    # Risk Level based on score
    def risk_level(score):
        if score <= 2:
            return "Low Risk"
        elif score <= 5:
            return "Moderate Risk"
        elif score <= 8:
            return "High Risk"
        else:
            return "Very High Risk"

    df["risk_level"] = df["risk_score"].apply(risk_level)

    # ──────────────────────────────────────────────
    # 5. Export cleaned dataset
    # ──────────────────────────────────────────────
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[SUCCESS] Cleaned dataset saved to: {OUTPUT_CSV}")
    print(f"[SUCCESS] Final shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # ──────────────────────────────────────────────
    # 6. Print summary statistics
    # ──────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  DATA SUMMARY")
    print(f"{'='*60}")
    print(f"\n  Columns in cleaned dataset:")
    for i, col in enumerate(df.columns, 1):
        print(f"    {i:2d}. {col}")

    print(f"\n  Disease Distribution:")
    disease_dist = df["diagnosis"].value_counts()
    for label, count in disease_dist.items():
        pct = count / len(df) * 100
        print(f"    {label}: {count} ({pct:.1f}%)")

    print(f"\n  Gender Distribution:")
    gender_dist = df["sex_label"].value_counts()
    for label, count in gender_dist.items():
        pct = count / len(df) * 100
        print(f"    {label}: {count} ({pct:.1f}%)")

    print(f"\n  Age Group Distribution:")
    age_dist = df["age_group"].value_counts().sort_index()
    for label, count in age_dist.items():
        pct = count / len(df) * 100
        print(f"    {label}: {count} ({pct:.1f}%)")

    print(f"\n  Risk Level Distribution:")
    risk_dist = df["risk_level"].value_counts()
    for label, count in risk_dist.items():
        pct = count / len(df) * 100
        print(f"    {label}: {count} ({pct:.1f}%)")

    print(f"\n  Key Statistics:")
    print(f"    Avg Age:              {df['age'].mean():.1f} years")
    print(f"    Avg Cholesterol:      {df['chol'].mean():.1f} mg/dl")
    print(f"    Avg Blood Pressure:   {df['trestbps'].mean():.1f} mm Hg")
    print(f"    Avg Max Heart Rate:   {df['thalach'].mean():.1f} bpm")
    print(f"    Avg Risk Score:       {df['risk_score'].mean():.1f}")


if __name__ == "__main__":
    prepare_data()
