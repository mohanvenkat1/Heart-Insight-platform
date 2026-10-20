# HeartInsight — Comprehensive Cardiovascular Datasets Review

## 1. Executive Summary

As part of the HeartInsight analytics and data engineering platform upgrade, the repository has been expanded with a harmonized collection of cardiovascular datasets and reference documentation. These resources are organized systematically across the `data/` and `docs/` directories.

```
HeartDisease/
├── data/
│   ├── heart.csv                          <- Active primary dataset (310 rows)
│   ├── raw/
│   │   ├── heart_raw.csv                  <- Audited raw snapshot preserved by pipeline
│   │   └── cleveland_303.csv              <- Canonical 303-patient UCI Cleveland benchmark
│   ├── cleaned/
│   │   └── heart_cleaned.csv              <- Quality-validated and cleaned records
│   ├── curated/
│   │   ├── heart_curated.csv              <- Enriched dataset with 14 clinical derived metrics
│   │   └── heart_curated.parquet          <- High-performance columnar store for DuckDB
│   └── benchmarks/
│       ├── README.md                      <- Dataset catalog and schema dictionary
│       ├── heart_attack_cleveland_303.csv <- Canonical Cleveland cohort
│       ├── heart_disease_extended_1025.csv<- Expanded 1,025-patient cohort
│       ├── heart_failure_multi_center_918.csv <- 5-center international study (918 rows)
│       ├── heart_statlog_cleveland_hungary_1190.csv <- 1,190 patient harmonized records
│       ├── heart_failure_clinical_records_299.csv   <- Chicco & Jurman survival study (299 rows)
│       └── heart_attack_risk_factors_9651.csv       <- Lifestyle & biomarker study (9,651 rows)
└── docs/
    ├── problem_statement.md
    ├── literature_survey.md
    ├── tableau_guide.md
    ├── documentation.pdf                  <- Reference project documentation
    ├── Heart Disease Prediction - Jupyter Notebook.pdf <- Exploratory data analysis notebook
    └── datasets_overview.md               <- This review document
```

---

## 2. Review of Added Datasets

### A. Primary Clinical Cohorts (Coronary Artery Disease)

1. **`heart_attack_cleveland_303.csv` (UCI Cleveland Gold Standard)**
   - **Size**: 303 rows x 14 columns
   - **Relevance**: This is the canonical dataset gathered by Dr. Robert Detrano at the Cleveland Clinic. It is the direct foundation of the literature cited in `docs/literature_survey.md`.
   - **Characteristics**: 0 null values, 1 duplicated record (patient #164). 165 positive disease cases (54.5%) and 138 negative cases (45.5%).
   - **How used**: Serves as our primary benchmark to reconcile the historical `data/heart.csv` (which had 310 records due to 7 duplicated entries).

2. **`heart_disease_extended_1025.csv` (Expanded Cleveland Cohort)**
   - **Size**: 1,025 rows x 14 columns
   - **Relevance**: Extensively used in modern machine learning benchmarks to avoid overfitting on small 300-row samples. It contains textual categorical labels (e.g. `Male`, `typical angina`, `reversable defect`).
   - **How used**: Cross-validation benchmark to evaluate model stability when moving from 300 to 1,000+ observations.

3. **`heart_statlog_cleveland_hungary_1190.csv` (Harmonized 3-Center Cohort)**
   - **Size**: 1,190 rows x 12 columns
   - **Relevance**: Merges Cleveland (USA), Hungarian Institute of Cardiology (Budapest), and the Statlog Heart project.
   - **How used**: Multi-center validation to verify whether risk scoring algorithms hold across different national healthcare systems.

4. **`heart_failure_multi_center_918.csv` (5-Center International Study)**
   - **Size**: 918 rows x 12 columns
   - **Relevance**: Compiled by Federico Tartaglia from 5 combined heart disease datasets (Cleveland, Hungarian, Switzerland, Long Beach VA, and Statlog).
   - **How used**: Evaluates diagnostic performance when angiographic fluoroscopy (`ca`) and thallium scintigraphy (`thal`) are unavailable in routine emergency triage.

---

### B. Specialized Clinical & Survival Cohorts

5. **`heart_failure_clinical_records_299.csv` (Heart Failure Survival & Mortality)**
   - **Size**: 299 rows x 13 columns
   - **Relevance**: Published by Chicco & Jurman in *BMC Medical Informatics and Decision Making* (2020). Tracks patients with heart failure during follow-up.
   - **Key Clinical Markers**: Serum creatinine, ejection fraction (EF%), follow-up time, and survival outcome (`DEATH_EVENT`).
   - **How used**: Secondary clinical analysis module for mortality risk stratification and renal-cardiac interaction analysis.

6. **`heart_attack_risk_factors_9651.csv` (Population-Level Biomarkers & Lifestyle)**
   - **Size**: 9,651 rows x 27 columns
   - **Relevance**: Represents modern preventive cardiology factors: Troponin, CK-MB enzyme levels, sedentary hours, sleep patterns, dietary habits, and stress indices.
   - **How used**: Preventive health awareness modeling, educational simulations, and lifestyle impact visualization in the web application.

---

## 3. Reference Documentation Added to `docs/`

1. **`documentation.pdf`**:
   - Comprehensive technical documentation outlining clinical definitions, data preprocessing guidelines, and algorithmic flows.
2. **`Heart Disease Prediction - Jupyter Notebook.pdf`**:
   - Step-by-step exploratory data analysis (EDA), univariate and bivariate distributions, correlation heatmaps, and initial predictive modeling prototypes.
