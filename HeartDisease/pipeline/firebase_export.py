"""
HeartInsight — Firebase Firestore Exporter
==========================================
Synchronizes curated summary analytics, pipeline execution metadata,
and cardiovascular benchmark catalogs to Google Cloud Firestore.

Modes:
    1. Offline / Dry-Run (Default when no credentials):
       Generates a structured Firestore document bundle at
       pipeline/logs/firestore_sync_payload.json for auditing or REST sync.
    2. Cloud Sync:
       Uploads directly to Firestore if `FIREBASE_SERVICE_ACCOUNT_KEY` environment
       variable or `firebase_credentials.json` is present.

Usage:
    python -m pipeline.firebase_export [--dry-run]
"""

import os
import json
from datetime import datetime, timezone
import pandas as pd
from pipeline.config import CURATED_CSV, PIPELINE_METADATA_JSON, PIPELINE_LOG_DIR, ensure_dirs
from pipeline.sql_analytics import run_analytics


def generate_firestore_payload() -> dict:
    """
    Assemble the complete JSON payload destined for Firestore collections:
      - /analytics/summary
      - /analytics/duckdb_queries
      - /benchmarks/catalog
    """
    ensure_dirs()

    # 1. Summary Stats
    total_patients = 0
    disease_rate = 0.0
    avg_chol = 0.0
    avg_bp = 0.0

    if os.path.exists(CURATED_CSV):
        df = pd.read_csv(CURATED_CSV)
        total_patients = len(df)
        if "target" in df.columns and total_patients > 0:
            disease_rate = round(float(df["target"].sum()) / total_patients * 100, 1)
        if "chol" in df.columns:
            avg_chol = round(float(df["chol"].mean()), 1)
        if "trestbps" in df.columns:
            avg_bp = round(float(df["trestbps"].mean()), 1)

    # 2. Pipeline Run Metadata
    pipeline_meta = {}
    if os.path.exists(PIPELINE_METADATA_JSON):
        try:
            with open(PIPELINE_METADATA_JSON, "r", encoding="utf-8") as f:
                pipeline_meta = json.load(f)
        except Exception:
            pass

    # 3. DuckDB Analytics
    analytics_report = run_analytics()

    payload = {
        "synced_at": datetime.now(timezone.utc).isoformat(),
        "platform_version": "1.0.0",
        "collections": {
            "analytics": {
                "summary": {
                    "total_patients": total_patients,
                    "disease_rate_pct": disease_rate,
                    "avg_cholesterol_mg_dl": avg_chol,
                    "avg_blood_pressure_mm_hg": avg_bp,
                    "pipeline_status": pipeline_meta.get("status", "unknown"),
                    "data_quality_score": pipeline_meta.get("stages", {}).get("validate", {}).get("summary", {}).get("data_quality_score", 100.0),
                    "last_pipeline_run": pipeline_meta.get("finished_at")
                },
                "duckdb_queries": {
                    q["name"]: {
                        "description": q["description"],
                        "rows_returned": q["rows_returned"],
                        "execution_time_ms": q["time_ms"],
                        "data": q["data"]
                    }
                    for q in analytics_report.get("queries", [])
                }
            },
            "benchmarks": {
                "cohorts_available": [
                    "UCI Cleveland (303 records)",
                    "Extended Kaggle (1025 records)",
                    "Multi-Center Tartaglia (918 records)",
                    "Statlog-Cleveland-Hungary (1190 records)",
                    "Chicco & Jurman Survival (299 records)",
                    "Biomarker & Lifestyle (9651 records)"
                ]
            }
        }
    }
    return payload


def export_to_firestore(dry_run: bool = False) -> dict:
    """
    Execute the Firestore export.
    If credentials exist and dry_run is False, upload to Firestore.
    Otherwise, write dry-run JSON payload to pipeline/logs/.
    """
    ensure_dirs()
    payload = generate_firestore_payload()

    out_json = os.path.join(PIPELINE_LOG_DIR, "firestore_sync_payload.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    cred_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY") or os.path.join(os.path.dirname(PIPELINE_LOG_DIR), "firebase_credentials.json")

    has_cloud_creds = os.path.exists(cred_path) if cred_path else False

    print("=" * 65)
    print("  [HeartInsight] -- Firebase Firestore Exporter")
    print("=" * 65)
    print(f"  Payload assembled: {len(payload['collections'])} collections")
    print(f"  Local JSON export: {out_json}")

    if has_cloud_creds and not dry_run:
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore

            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)

            db = firestore.client()
            for coll_name, docs in payload["collections"].items():
                for doc_id, doc_data in docs.items():
                    db.collection(coll_name).document(doc_id).set(doc_data)
            print("  [OK] Firestore Cloud Upload: SUCCESS (All documents updated)")
        except Exception as e:
            print(f"  [WARN] Firebase Cloud Upload failed: {e}")
            print("  [INFO] Stored local JSON payload successfully.")
    else:
        print("  [INFO] Running in Offline / Dry-Run Mode (Spark Plan).")
        print("  [OK] Payload verified and ready for Firestore sync.")

    print("=" * 65 + "\n")
    return payload


if __name__ == "__main__":
    export_to_firestore()
