"""
Heart Disease Analysis - Database Creation Script
===================================================
This script creates an SQLite database from the UCI Heart Disease CSV dataset.
It creates the 'heart_disease' table with proper schema and loads all records.

Usage:
    python database/create_db.py
"""

import sqlite3
import csv
import os
import sys

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "heart.csv")
DB_PATH = os.path.join(BASE_DIR, "database", "heart_disease.db")


def create_database():
    """Create SQLite database and load heart disease data from CSV."""

    # Remove existing database if present
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[INFO] Removed existing database: {DB_PATH}")

    # Connect to SQLite (creates the file)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("[INFO] Connected to SQLite database.")

    # ──────────────────────────────────────────────
    # 1. Create the heart_disease table
    # ──────────────────────────────────────────────
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heart_disease (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            age         INTEGER NOT NULL,
            sex         INTEGER NOT NULL,          -- 0 = Female, 1 = Male
            cp          INTEGER NOT NULL,          -- Chest pain type (0-3)
            trestbps    INTEGER NOT NULL,          -- Resting blood pressure (mm Hg)
            chol        INTEGER NOT NULL,          -- Serum cholesterol (mg/dl)
            fbs         INTEGER NOT NULL,          -- Fasting blood sugar > 120 mg/dl
            restecg     INTEGER NOT NULL,          -- Resting ECG results (0-2)
            thalach     INTEGER NOT NULL,          -- Max heart rate achieved
            exang       INTEGER NOT NULL,          -- Exercise induced angina
            oldpeak     REAL    NOT NULL,           -- ST depression
            slope       INTEGER NOT NULL,          -- Slope of peak exercise ST
            ca          INTEGER NOT NULL,          -- Number of major vessels (0-3)
            thal        INTEGER NOT NULL,          -- Thalassemia type
            target      INTEGER NOT NULL           -- 0 = No disease, 1 = Disease
        );
    """)
    print("[INFO] Table 'heart_disease' created successfully.")

    # ──────────────────────────────────────────────
    # 2. Load CSV data into the table
    # ──────────────────────────────────────────────
    if not os.path.exists(CSV_PATH):
        print(f"[ERROR] CSV file not found: {CSV_PATH}")
        sys.exit(1)

    row_count = 0
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cursor.execute("""
                    INSERT INTO heart_disease 
                    (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    int(row["age"]),
                    int(row["sex"]),
                    int(row["cp"]),
                    int(row["trestbps"]),
                    int(row["chol"]),
                    int(row["fbs"]),
                    int(row["restecg"]),
                    int(row["thalach"]),
                    int(row["exang"]),
                    float(row["oldpeak"]),
                    int(row["slope"]),
                    int(row["ca"]),
                    int(row["thal"]),
                    int(row["target"]),
                ))
                row_count += 1
            except (ValueError, KeyError) as e:
                print(f"[WARN] Skipping row due to error: {e}")
                continue

    conn.commit()
    print(f"[INFO] Loaded {row_count} records into 'heart_disease' table.")

    # ──────────────────────────────────────────────
    # 3. Verify the data
    # ──────────────────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM heart_disease")
    total = cursor.fetchone()[0]
    print(f"[INFO] Verification: {total} total records in database.")

    cursor.execute("SELECT * FROM heart_disease LIMIT 5")
    print("\n[INFO] Sample records (first 5):")
    print(f"{'ID':<5} {'Age':<5} {'Sex':<5} {'CP':<5} {'BP':<6} {'Chol':<6} {'FBS':<5} {'ECG':<5} {'HR':<5} {'Exang':<7} {'OldPk':<7} {'Slope':<7} {'CA':<5} {'Thal':<6} {'Target'}")
    print("-" * 90)
    for row in cursor.fetchall():
        print(f"{row[0]:<5} {row[1]:<5} {row[2]:<5} {row[3]:<5} {row[4]:<6} {row[5]:<6} {row[6]:<5} {row[7]:<5} {row[8]:<5} {row[9]:<7} {row[10]:<7} {row[11]:<7} {row[12]:<5} {row[13]:<6} {row[14]}")

    conn.close()
    print(f"\n[SUCCESS] Database created at: {DB_PATH}")
    print(f"[SUCCESS] Total records: {total}")


if __name__ == "__main__":
    create_database()
