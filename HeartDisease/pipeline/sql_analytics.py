"""
HeartInsight — SQL Analytics Stage
=====================================
Run analytical queries on the curated Parquet file using DuckDB.
DuckDB reads Parquet directly — no separate database file needed.

Queries match the original sql_operations.py analysis but run against
the cleaned/enriched dataset and use DuckDB instead of SQLite.

Returns:
    dict: Query results and execution metadata.
"""

import duckdb
import os
from pipeline.config import CURATED_PARQUET


# ── Analytical Queries ──
# Each tuple: (name, SQL template, description)
# The SQL uses 'heart' as the table alias for the Parquet file.
QUERIES = [
    (
        "overall_stats",
        """
        SELECT
            COUNT(*) AS total_patients,
            ROUND(AVG(age), 1) AS avg_age,
            MIN(age) AS min_age,
            MAX(age) AS max_age,
            ROUND(AVG(chol), 1) AS avg_cholesterol,
            ROUND(AVG(trestbps), 1) AS avg_blood_pressure,
            ROUND(AVG(thalach), 1) AS avg_max_heart_rate,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS disease_count,
            SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS no_disease_count,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        """,
        "Overall dataset statistics",
    ),
    (
        "disease_by_gender",
        """
        SELECT
            sex_label AS gender,
            COUNT(*) AS total,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS with_disease,
            SUM(CASE WHEN target = 0 THEN 1 ELSE 0 END) AS without_disease,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        GROUP BY sex_label
        ORDER BY gender
        """,
        "Heart disease breakdown by gender",
    ),
    (
        "stats_by_age_group",
        """
        SELECT
            age_group,
            COUNT(*) AS patient_count,
            ROUND(AVG(chol), 1) AS avg_cholesterol,
            ROUND(AVG(trestbps), 1) AS avg_bp,
            ROUND(AVG(thalach), 1) AS avg_max_hr,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        GROUP BY age_group
        ORDER BY age_group
        """,
        "Statistics by age group",
    ),
    (
        "disease_by_chest_pain",
        """
        SELECT
            cp_label AS chest_pain_type,
            COUNT(*) AS total,
            SUM(CASE WHEN target = 1 THEN 1 ELSE 0 END) AS with_disease,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        GROUP BY cp_label
        ORDER BY disease_rate_pct DESC
        """,
        "Disease prevalence by chest pain type",
    ),
    (
        "risk_level_distribution",
        """
        SELECT
            risk_level,
            COUNT(*) AS patient_count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS percentage
        FROM heart
        GROUP BY risk_level
        ORDER BY
            CASE risk_level
                WHEN 'Low Risk' THEN 1
                WHEN 'Moderate Risk' THEN 2
                WHEN 'High Risk' THEN 3
                WHEN 'Very High Risk' THEN 4
            END
        """,
        "Patient distribution by risk level",
    ),
    (
        "cholesterol_bp_crosstab",
        """
        SELECT
            cholesterol_category,
            bp_category,
            COUNT(*) AS patient_count,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        GROUP BY cholesterol_category, bp_category
        ORDER BY disease_rate_pct DESC
        """,
        "Disease rate by cholesterol × blood pressure category",
    ),
    (
        "exercise_angina_impact",
        """
        SELECT
            exang_label AS exercise_angina,
            COUNT(*) AS total,
            ROUND(AVG(thalach), 1) AS avg_max_hr,
            ROUND(AVG(oldpeak), 2) AS avg_st_depression,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        GROUP BY exang_label
        """,
        "Impact of exercise-induced angina",
    ),
    (
        "high_risk_patients",
        """
        SELECT
            COUNT(*) AS high_risk_count,
            ROUND(AVG(age), 1) AS avg_age,
            ROUND(AVG(chol), 1) AS avg_chol,
            ROUND(AVG(trestbps), 1) AS avg_bp,
            ROUND(SUM(CASE WHEN target = 1 THEN 1.0 ELSE 0 END) / COUNT(*) * 100, 1) AS disease_rate_pct
        FROM heart
        WHERE chol >= 240 AND trestbps >= 140
        """,
        "Profile of high-risk patients (high cholesterol + high BP)",
    ),
]


def run_analytics(parquet_path: str | None = None) -> dict:
    """
    Execute all analytical queries using DuckDB on the curated Parquet.

    Parameters
    ----------
    parquet_path : str, optional
        Path to the curated Parquet file. Defaults to config.CURATED_PARQUET.

    Returns
    -------
    report : dict
        Query results and execution metadata.
    """
    source = parquet_path or CURATED_PARQUET
    report = {
        "stage": "sql_analytics",
        "status": "pending",
        "source": source,
        "queries": [],
    }

    if not os.path.exists(source):
        report["status"] = "error"
        report["issues"] = [f"Parquet file not found: {source}"]
        raise FileNotFoundError(f"Curated Parquet not found: {source}")

    # ── Create DuckDB in-memory connection ──
    con = duckdb.connect(database=":memory:")

    # Register the Parquet file as a table named 'heart'
    con.execute(f"CREATE VIEW heart AS SELECT * FROM read_parquet('{source.replace(chr(92), '/')}')")

    print(f"[ANALYTICS] Running {len(QUERIES)} analytical queries on DuckDB...")

    for name, sql, description in QUERIES:
        import time
        start = time.perf_counter()
        result = con.execute(sql).fetchdf()
        elapsed_ms = round((time.perf_counter() - start) * 1000, 3)

        query_result = {
            "name": name,
            "description": description,
            "rows_returned": len(result),
            "time_ms": elapsed_ms,
            "columns": list(result.columns),
            "data": result.to_dict(orient="records"),
        }
        report["queries"].append(query_result)
        print(f"[ANALYTICS]    [OK] {name:<30s} -> {len(result):>4d} rows in {elapsed_ms:.3f} ms")

    con.close()
    report["status"] = "success"
    print(f"[ANALYTICS] [OK] All {len(QUERIES)} queries completed successfully")

    return report
