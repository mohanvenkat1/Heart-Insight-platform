# Cardiovascular Benchmark Datasets

This directory contains external benchmark and reference datasets utilized for cross-dataset validation, cohort comparisons, and model generalization in the HeartInsight platform.

## Summary of Datasets

| Filename | Records | Features | Target Variable | Primary Clinical Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `heart_attack_cleveland_303.csv` | 303 | 14 | `target` (0 = <50% stenosis, 1 = >=50% stenosis) | Gold-standard UCI Cleveland reference cohort. Core baseline for angiographic CAD detection. |
| `heart_disease_extended_1025.csv` | 1,025 | 14 | `target` (0/1 or No/Yes) | Extended Kaggle replication of Cleveland dataset with categorical labels. |
| `heart_failure_multi_center_918.csv` | 918 | 12 | `HeartDisease` (0 = Normal, 1 = Heart Disease) | 5-hospital combined study (Cleveland, Hungarian, Switzerland, Long Beach VA, Statlog). Tests model portability. |
| `heart_statlog_cleveland_hungary_1190.csv` | 1,190 | 12 | `target` (0/1) | Harmonized Statlog, Cleveland, and Hungary dataset for cross-institutional analysis. |
| `heart_failure_clinical_records_299.csv` | 299 | 13 | `DEATH_EVENT` (0/1) | Chicco & Jurman clinical records for heart failure survival analysis (ejection fraction, serum creatinine). |
| `heart_attack_risk_factors_9651.csv` | 9,651 | 27 | `Heart Attack Risk (Binary)` (0/1) | Comprehensive lifestyle, socioeconomic, and biomarker risk factors (Troponin, CK-MB, BMI, sleep, stress). |

---

## Detailed Clinical Schemas

### 1. `heart_attack_cleveland_303.csv` (UCI Cleveland Gold Standard)
- **Origin**: Dr. Robert Detrano, V.A. Medical Center, Long Beach and Cleveland Clinic Foundation.
- **Attributes**:
  1. `age`: Age in years
  2. `sex`: Sex (1 = male, 0 = female)
  3. `cp`: Chest pain type (0 = typical angina, 1 = atypical angina, 2 = non-anginal pain, 3 = asymptomatic)
  4. `trestbps`: Resting blood pressure (mm Hg on admission)
  5. `chol`: Serum cholesterol in mg/dl
  6. `fbs`: Fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
  7. `restecg`: Resting ECG results (0 = normal, 1 = ST-T wave abnormality, 2 = probable/definite left ventricular hypertrophy)
  8. `thalach`: Maximum heart rate achieved during exercise stress testing
  9. `exang`: Exercise-induced angina (1 = yes, 0 = no)
  10. `oldpeak`: ST depression induced by exercise relative to rest
  11. `slope`: Slope of peak exercise ST segment (0 = upsloping, 1 = flat, 2 = downsloping)
  12. `ca`: Number of major vessels (0-3) colored by fluoroscopy
  13. `thal`: Thallium scintigraphy (1 = normal, 2 = fixed defect, 3 = reversible defect)
  14. `target`: Presence of heart disease (1 = angiographic disease >= 50% diameter narrowing, 0 = absence)

### 2. `heart_failure_clinical_records_299.csv` (Survival Analysis Cohort)
- **Origin**: Davide Chicco, Giuseppe Jurman, BMC Medical Informatics and Decision Making (2020).
- **Attributes**:
  - `age`: Patient age
  - `anaemia`: Decrease of red blood cells or hemoglobin (0/1)
  - `creatinine_phosphokinase`: Level of the CPK enzyme in blood (mcg/L)
  - `diabetes`: Patient diagnosed with diabetes (0/1)
  - `ejection_fraction`: Percentage of blood leaving the heart at each contraction (%)
  - `high_blood_pressure`: Patient diagnosed with hypertension (0/1)
  - `platelets`: Platelets in the blood (kiloplatelets/mL)
  - `serum_creatinine`: Level of serum creatinine in blood (mg/dL)
  - `serum_sodium`: Level of serum sodium in blood (mEq/L)
  - `sex`: Woman (0) or man (1)
  - `smoking`: Patient smokes (0/1)
  - `time`: Follow-up period (days)
  - `DEATH_EVENT`: Patient deceased during follow-up period (0/1)

### 3. `heart_attack_risk_factors_9651.csv` (Biomarkers & Lifestyle)
- **Attributes**:
  - Demographic & Clinical: Age, Gender, Systolic BP, Diastolic BP, Heart Rate, BMI, Diabetes, Family History, Previous Heart Problems, Medication Use.
  - Biomarkers: Cholesterol, Triglycerides, Blood Sugar, CK-MB, Troponin.
  - Behavioral & Lifestyle: Smoking, Alcohol Consumption, Exercise Hours Per Week, Physical Activity Days, Diet, Stress Level, Sedentary Hours Per Day, Sleep Hours Per Day, Income.
  - Outcome: Heart Attack Risk (Binary: 0/1) and Textual Severity.
