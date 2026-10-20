# HeartInsight — Cloud-Connected Cardiovascular Analytics & Data Engineering Platform

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-lightgrey.svg)](https://flask.palletsprojects.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.2.2-yellow.svg)](https://duckdb.org/)
[![Firebase](https://img.shields.io/badge/Firebase-Hosting%20%7C%20Firestore-orange.svg)](https://firebase.google.com/)
[![Tests](https://img.shields.io/badge/Tests-25%20Passed-brightgreen.svg)]()

## 📋 Project Overview

**HeartInsight** is an enterprise-grade cardiovascular data engineering and clinical analytics platform. Upgraded from an initial Tableau visualization project, HeartInsight now provides a repeatable multi-stage data pipeline, high-performance analytical SQL powered by DuckDB, Parquet columnar storage, Firebase cloud hosting integration, an interactive Flask analytics application, and a curated library of multi-center cardiovascular benchmark datasets.

---

## 🛠️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Cloud Presentation & Static Edge                      │
│             Firebase Hosting (Public Landing & Risk Simulator)         │
├────────────────────────────────────────────────────────────────────────┤
│                     Local Analytics Application                        │
│          Flask 3.1 Web App  (Dashboard, Live Pipeline, Datasets)       │
│                  Tableau Public Embedded Workbooks                     │
├────────────────────────────────────────────────────────────────────────┤
│                 Vectorized Analytical Query Engine                     │
│                DuckDB (Direct SQL on Parquet, <10ms)                   │
├────────────────────────────────────────────────────────────────────────┤
│                     Repeatable Data Pipeline                           │
│  Ingest ──> Validate (Quality Score) ──> Transform ──> Export (Parquet)│
├────────────────────────────────────────────────────────────────────────┤
│                     Data Lake & Benchmark Storage                      │
│  • Primary Cohort: data/heart.csv (310 rows)                           │
│  • Canonical Gold Standard: data/raw/cleveland_303.csv (303 rows)      │
│  • Multi-Center Benchmarks: data/benchmarks/ (6 cohorts, 13,000+ rows) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
HeartDisease/
├── README.md                            # Comprehensive platform documentation
├── requirements.txt                     # Pinned core, pipeline, and testing dependencies
├── firebase.json                        # Firebase Hosting & Firestore configuration
├── .firebaserc                          # Firebase project definition
├── firestore.rules                      # Firestore security rules
│
├── data/
│   ├── heart.csv                        # Primary active dataset
│   ├── raw/
│   │   ├── heart_raw.csv                # Immutable ingestion snapshot
│   │   └── cleveland_303.csv            # Canonical 303-patient UCI Cleveland benchmark
│   ├── cleaned/
│   │   └── heart_cleaned.csv            # Cleaned data
│   ├── curated/
│   │   ├── heart_curated.csv            # Curated data with 14 clinical features
│   │   └── heart_curated.parquet        # Columnar format for DuckDB
│   └── benchmarks/
│       ├── README.md                    # Benchmark manifest & schema dictionary
│       ├── heart_attack_cleveland_303.csv
│       ├── heart_disease_extended_1025.csv
│       ├── heart_failure_multi_center_918.csv
│       ├── heart_statlog_cleveland_hungary_1190.csv
│       ├── heart_failure_clinical_records_299.csv
│       └── heart_attack_risk_factors_9651.csv
│
├── docs/
│   ├── problem_statement.md             # Clinical & business problem definition
│   ├── literature_survey.md             # Review of peer-reviewed cardiovascular studies
│   ├── tableau_guide.md                 # Visual analytics step-by-step guide
│   ├── datasets_overview.md             # In-depth clinical review of all datasets
│   ├── documentation.pdf                # Reference system documentation
│   └── Heart Disease Prediction - Jupyter Notebook.pdf # Reference EDA notebook
│
├── pipeline/
│   ├── config.py                        # Path definitions, schemas, and clinical ranges
│   ├── ingest.py                        # Ingestion and schema auditing
│   ├── validate.py                      # Quality scoring and physiological bounds
│   ├── transform.py                     # Feature enrichment (14 derived attributes)
│   ├── export.py                        # Multi-format exporter (CSV + Parquet)
│   ├── sql_analytics.py                 # DuckDB analytical query suite (8 queries)
│   ├── firebase_export.py               # Firestore cloud sync & dry-run payload
│   ├── run_pipeline.py                  # End-to-end pipeline orchestrator
│   └── logs/
│       ├── last_run.json                # Pipeline run telemetry and reconciliation
│       └── firestore_sync_payload.json  # Exported Firestore document bundle
│
├── webapp/
│   ├── app.py                           # Upgraded Flask application
│   ├── static/                          # CSS design system & JavaScript
│   └── templates/
│       ├── base.html                    # Glassmorphic layout & navigation
│       ├── index.html                   # Overview and KPI counters
│       ├── dashboard.html               # Tableau dashboard embed
│       ├── story.html                   # Tableau story embed
│       ├── data.html                    # Interactive data table with search/filter
│       ├── analysis.html                # Chart.js clinical visualizations
│       ├── pipeline.html                # Live pipeline monitoring & DuckDB cache
│       ├── datasets.html                # Benchmark datasets catalog & dictionary
│       └── calculator.html              # Interactive heuristic risk scoring tool
│
├── firebase/
│   └── public/
│       └── index.html                   # Static cloud landing page for Firebase Hosting
│
└── tests/
    ├── test_pipeline.py                 # 7 tests for pipeline stages & reconciliation
    ├── test_webapp.py                   # 10 tests for Flask routes & JSON APIs
    └── test_datasets.py                 # 8 tests for benchmark cohorts and docs
```

---

## ⚡ Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repository-url>
cd HeartDisease

# Install all dependencies
pip install -r requirements.txt
```

### 2. Execute the Data Pipeline

Run the automated 5-stage data engineering pipeline:

```bash
python -m pipeline.run_pipeline
```

Output:
- Ingestion, validation, and transformation runs in under **300 ms**
- Computes data quality scores and flags duplicates/outliers
- Exports curated Parquet and executes 8 DuckDB analytical queries
- Saves run metadata to `pipeline/logs/last_run.json`

### 3. Launch the Web Application

```bash
python webapp/app.py
```

Open `http://localhost:5000` in your browser to access:
- **Home**: Executive overview, KPI stats, clinical scenarios
- **Dashboard & Story**: Tableau Public embeds with graceful fallbacks
- **Data**: Searchable, filterable client-side data explorer
- **Analysis**: Chart.js distributions, age brackets, chest pain cross-tabs
- **Pipeline**: Live pipeline telemetry, stage durations, and DuckDB query cache
- **Datasets**: Cardiovascular benchmark library with schemas and cohort metadata
- **Calculator**: Interactive patient risk factor evaluation tool

### 4. Run the Test Suite

```bash
pytest tests/
```

Runs 25 automated tests across all pipeline stages, Flask routes, REST APIs, and dataset files.

---

## ☁️ Firebase Cloud Integration

HeartInsight is configured for zero-cost deployment on the **Firebase Spark Plan**:

1. **Static Hosting**: Deploy the cloud landing page to Firebase Hosting:
   ```bash
   npm install -g firebase-tools
   firebase login
   firebase deploy --only hosting
   ```
2. **Firestore Sync**: Export curated metrics and query summaries to Firestore:
   ```bash
   python -m pipeline.firebase_export
   ```
   *(Runs automatically in dry-run mode when cloud credentials are not supplied, saving an audited payload to `pipeline/logs/firestore_sync_payload.json`)*

---

## 📚 Datasets & Reference Documentation

The repository houses 6 cardiovascular datasets and reference research materials:
1. `heart_attack_cleveland_303.csv`: UCI Cleveland reference cohort (303 records, 14 features)
2. `heart_disease_extended_1025.csv`: Expanded multi-sample cohort (1,025 records)
3. `heart_failure_multi_center_918.csv`: 5-hospital international study (918 records)
4. `heart_statlog_cleveland_hungary_1190.csv`: Cross-national cohort (1,190 records)
5. `heart_failure_clinical_records_299.csv`: Chicco & Jurman survival study (299 records)
6. `heart_attack_risk_factors_9651.csv`: Lifestyle, biomarker, and Troponin study (9,651 records)
7. `docs/documentation.pdf`: System documentation
8. `docs/Heart Disease Prediction - Jupyter Notebook.pdf`: Exploratory analysis notebook

See `data/benchmarks/README.md` and `docs/datasets_overview.md` for complete schema breakdowns and clinical evidence.

---

## 🧑‍💻 Author & Lead Architect

**Dulapalli Mohan Venkat**  
*Healthcare Analytics Architect, Data Engineer & Platform Developer*

---

## 📜 License & Disclaimers

This project is developed for educational and data engineering purposes. Interactive risk scores and algorithms are non-clinical heuristics and are **NOT** a substitute for certified medical diagnosis or clinical judgment.
