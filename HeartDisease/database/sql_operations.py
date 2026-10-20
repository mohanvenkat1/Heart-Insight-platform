"""
Heart Disease Analysis - SQL Operations
=========================================
Demonstrates various SQL operations on the heart_disease database:
- SELECT queries
- AGGREGATE functions (COUNT, AVG, MAX, MIN)
- GROUP BY and HAVING
- FILTER with WHERE clauses
- Calculated fields and CASE expressions
- Cross-tabulation queries

Usage:
    python database/sql_operations.py
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "heart_disease.db")


def print_separator(title):
    """Print a formatted section separator."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_table(headers, rows):
    """Print formatted table output."""
    col_widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0)) + 2 for i, h in enumerate(headers)]
    header_line = "".join(str(h).ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print("".join(str(r).ljust(w) for r, w in zip(row, col_widths)))


def run_sql_operations():
    """Execute and display various SQL operations."""

    if not os.path.exists(DB_PATH):
        print("[ERROR] Database not found. Run create_db.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ──────────────────────────────────────────────
    # 1. Basic SELECT - All patients with heart disease
    # ──────────────────────────────────────────────
    print_separator("1. SELECT: Patients with Heart Disease")
    cursor.execute("""
        SELECT id, age, 
               CASE sex WHEN 1 THEN 'Male' ELSE 'Female' END AS gender,
               trestbps, chol, thalach, target
        FROM heart_disease 
        WHERE target = 1 
        LIMIT 10
    """)
    rows = cursor.fetchall()
    print_table(["ID", "Age", "Gender", "BP", "Chol", "MaxHR", "Target"], rows)
    print(f"\n  -> Showing first 10 of patients with heart disease")

    # ──────────────────────────────────────────────
    # 2. AGGREGATE - Overall Statistics
    # ──────────────────────────────────────────────
    print_separator("2. AGGREGATE: Overall Dataset Statistics")
    cursor.execute("""
        SELECT 
            COUNT(*) AS total_patients,
            ROUND(AVG(age), 1) AS avg_age,
            MIN(age) AS min_age,
            MAX(age) AS max_age,
            ROUND(AVG(chol), 1) AS avg_cholesterol,
            ROUND(AVG(trestbps), 1) AS avg_blood_pressure,
            ROUND(AVG(thalach), 1) AS avg_max_heart_rate,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS disease_count,
            SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS no_disease_count
        FROM heart_disease
    """)
    row = cursor.fetchone()
    print(f"  Total Patients:       {row[0]}")
    print(f"  Average Age:          {row[1]} years")
    print(f"  Age Range:            {row[2]} - {row[3]} years")
    print(f"  Avg Cholesterol:      {row[4]} mg/dl")
    print(f"  Avg Blood Pressure:   {row[5]} mm Hg")
    print(f"  Avg Max Heart Rate:   {row[6]} bpm")
    print(f"  With Disease:         {row[7]}")
    print(f"  Without Disease:      {row[8]}")
    print(f"  Disease Rate:         {round(row[7]/row[0]*100, 1)}%")

    # ──────────────────────────────────────────────
    # 3. GROUP BY - Disease count by Gender
    # ──────────────────────────────────────────────
    print_separator("3. GROUP BY: Heart Disease by Gender")
    cursor.execute("""
        SELECT 
            CASE sex WHEN 1 THEN 'Male' ELSE 'Female' END AS gender,
            COUNT(*) AS total,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS with_disease,
            SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS without_disease,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart_disease
        GROUP BY sex
    """)
    rows = cursor.fetchall()
    print_table(["Gender", "Total", "Disease", "No Disease", "Rate %"], rows)

    # ──────────────────────────────────────────────
    # 4. GROUP BY - Average Cholesterol by Age Group
    # ──────────────────────────────────────────────
    print_separator("4. GROUP BY: Avg Cholesterol by Age Group")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN age < 30 THEN '20-29'
                WHEN age < 40 THEN '30-39'
                WHEN age < 50 THEN '40-49'
                WHEN age < 60 THEN '50-59'
                WHEN age < 70 THEN '60-69'
                ELSE '70+'
            END AS age_group,
            COUNT(*) AS patient_count,
            ROUND(AVG(chol), 1) AS avg_cholesterol,
            ROUND(AVG(trestbps), 1) AS avg_bp,
            ROUND(AVG(thalach), 1) AS avg_max_hr
        FROM heart_disease
        GROUP BY age_group
        ORDER BY age_group
    """)
    rows = cursor.fetchall()
    print_table(["Age Group", "Count", "Avg Chol", "Avg BP", "Avg MaxHR"], rows)

    # ──────────────────────────────────────────────
    # 5. GROUP BY - Disease by Chest Pain Type
    # ──────────────────────────────────────────────
    print_separator("5. GROUP BY: Disease Prevalence by Chest Pain Type")
    cursor.execute("""
        SELECT 
            CASE cp 
                WHEN 0 THEN 'Typical Angina'
                WHEN 1 THEN 'Atypical Angina'
                WHEN 2 THEN 'Non-anginal Pain'
                WHEN 3 THEN 'Asymptomatic'
            END AS chest_pain_type,
            COUNT(*) AS total,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS with_disease,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart_disease
        GROUP BY cp
        ORDER BY disease_rate_pct DESC
    """)
    rows = cursor.fetchall()
    print_table(["Chest Pain Type", "Total", "Disease", "Rate %"], rows)

    # ──────────────────────────────────────────────
    # 6. FILTER - High-Risk Patients
    # ──────────────────────────────────────────────
    print_separator("6. FILTER: High-Risk Patients (Chol > 240 AND BP > 140)")
    cursor.execute("""
        SELECT id, age, 
               CASE sex WHEN 1 THEN 'Male' ELSE 'Female' END AS gender,
               trestbps, chol, thalach,
               CASE target WHEN 1 THEN 'Disease' ELSE 'No Disease' END AS diagnosis
        FROM heart_disease
        WHERE chol > 240 AND trestbps > 140
        ORDER BY chol DESC
        LIMIT 15
    """)
    rows = cursor.fetchall()
    print_table(["ID", "Age", "Gender", "BP", "Chol", "MaxHR", "Diagnosis"], rows)

    # ──────────────────────────────────────────────
    # 7. CALCULATED FIELDS - Risk Categories
    # ──────────────────────────────────────────────
    print_separator("7. CALCULATED FIELDS: Cholesterol & BP Risk Categories")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN chol < 200 THEN 'Desirable'
                WHEN chol < 240 THEN 'Borderline High'
                ELSE 'High'
            END AS chol_category,
            CASE 
                WHEN trestbps < 120 THEN 'Normal'
                WHEN trestbps < 130 THEN 'Elevated'
                WHEN trestbps < 140 THEN 'High Stage 1'
                ELSE 'High Stage 2'
            END AS bp_category,
            COUNT(*) AS patient_count,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart_disease
        GROUP BY chol_category, bp_category
        ORDER BY disease_rate_pct DESC
    """)
    rows = cursor.fetchall()
    print_table(["Cholesterol", "Blood Pressure", "Count", "Disease %"], rows)

    # ──────────────────────────────────────────────
    # 8. CROSS-TABULATION - Gender vs Chest Pain vs Disease
    # ──────────────────────────────────────────────
    print_separator("8. CROSS-TABULATION: Gender × Chest Pain × Disease")
    cursor.execute("""
        SELECT 
            CASE sex WHEN 1 THEN 'Male' ELSE 'Female' END AS gender,
            CASE cp 
                WHEN 0 THEN 'Typical Angina'
                WHEN 1 THEN 'Atypical Angina'
                WHEN 2 THEN 'Non-anginal Pain'
                WHEN 3 THEN 'Asymptomatic'
            END AS chest_pain,
            COUNT(*) AS total,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS disease,
            SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS no_disease
        FROM heart_disease
        GROUP BY sex, cp
        ORDER BY sex, cp
    """)
    rows = cursor.fetchall()
    print_table(["Gender", "Chest Pain", "Total", "Disease", "No Disease"], rows)

    # ──────────────────────────────────────────────
    # 9. HAVING - Age groups with high disease rates
    # ──────────────────────────────────────────────
    print_separator("9. HAVING: Age Groups with Disease Rate > 50%")
    cursor.execute("""
        SELECT 
            CASE 
                WHEN age < 30 THEN '20-29'
                WHEN age < 40 THEN '30-39'
                WHEN age < 50 THEN '40-49'
                WHEN age < 60 THEN '50-59'
                WHEN age < 70 THEN '60-69'
                ELSE '70+'
            END AS age_group,
            COUNT(*) AS total,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS disease_count,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate
        FROM heart_disease
        GROUP BY age_group
        HAVING disease_rate > 50
        ORDER BY disease_rate DESC
    """)
    rows = cursor.fetchall()
    print_table(["Age Group", "Total", "Disease", "Rate %"], rows)

    # ──────────────────────────────────────────────
    # 10. Exercise Angina Impact
    # ──────────────────────────────────────────────
    print_separator("10. ANALYSIS: Exercise Induced Angina Impact")
    cursor.execute("""
        SELECT 
            CASE exang WHEN 1 THEN 'Yes' ELSE 'No' END AS exercise_angina,
            COUNT(*) AS total,
            ROUND(AVG(thalach), 1) AS avg_max_hr,
            ROUND(AVG(oldpeak), 2) AS avg_st_depression,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate
        FROM heart_disease
        GROUP BY exang
    """)
    rows = cursor.fetchall()
    print_table(["Ex. Angina", "Total", "Avg MaxHR", "Avg ST Dep.", "Disease %"], rows)

    conn.close()
    print(f"\n{'='*70}")
    print("  All SQL operations completed successfully!")
    print(f"{'='*70}")


if __name__ == "__main__":
    run_sql_operations()
