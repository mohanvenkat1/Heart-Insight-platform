# Literature Survey: Heart Disease Analysis

## 1. Introduction

This literature survey reviews key research, datasets, and methodologies related to heart disease analysis and data visualization in healthcare. The survey covers the epidemiological background, the dataset origins, relevant analytical approaches, and the role of business intelligence tools like Tableau in healthcare analytics.

---

## 2. Epidemiological Background

### 2.1 Global Burden of Heart Disease

Heart disease, encompassing conditions such as coronary artery disease (CAD), heart failure, and arrhythmias, is the **leading cause of mortality worldwide**. According to the World Health Organization (WHO):

- **17.9 million people** die annually from cardiovascular diseases (CVDs)
- CVDs represent **32% of all global deaths**
- **85% of CVD deaths** are due to heart attacks and strokes
- Risk factors include tobacco use, unhealthy diet, physical inactivity, and harmful use of alcohol

> **Reference:** World Health Organization. (2023). *Cardiovascular Diseases (CVDs) Fact Sheet*. WHO.

### 2.2 Risk Factors

The American Heart Association (AHA) identifies the following modifiable and non-modifiable risk factors:

| Category | Risk Factors |
|----------|-------------|
| **Non-modifiable** | Age, Gender, Family History, Ethnicity |
| **Modifiable** | High cholesterol, High blood pressure, Smoking, Diabetes, Obesity, Physical inactivity |
| **Contributing** | Stress, Alcohol consumption, Poor diet |

> **Reference:** American Heart Association. (2023). *Understanding Your Risks to Prevent a Heart Attack*. AHA.

---

## 3. Dataset Background

### 3.1 UCI Heart Disease Dataset

The dataset used in this project originates from the **UCI Machine Learning Repository**, specifically the **Cleveland Heart Disease Database** contributed by:

- **Robert Detrano, M.D., Ph.D.** — V.A. Medical Center, Long Beach and Cleveland Clinic Foundation

The original dataset contains **76 attributes**, but published experiments typically use a **subset of 14 attributes** that have been found most relevant for predicting heart disease:

| # | Attribute | Type | Description |
|---|-----------|------|-------------|
| 1 | age | Numeric | Age in years |
| 2 | sex | Binary | 1 = Male, 0 = Female |
| 3 | cp | Categorical | Chest pain type (0-3) |
| 4 | trestbps | Numeric | Resting blood pressure |
| 5 | chol | Numeric | Serum cholesterol (mg/dl) |
| 6 | fbs | Binary | Fasting blood sugar > 120 mg/dl |
| 7 | restecg | Categorical | Resting ECG results |
| 8 | thalach | Numeric | Maximum heart rate achieved |
| 9 | exang | Binary | Exercise induced angina |
| 10 | oldpeak | Numeric | ST depression (exercise vs rest) |
| 11 | slope | Categorical | Slope of peak exercise ST segment |
| 12 | ca | Numeric | Number of major vessels (fluoroscopy) |
| 13 | thal | Categorical | Thalassemia type |
| 14 | target | Binary | Heart disease diagnosis |

> **Reference:** Detrano, R., et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease*. American Journal of Cardiology, 64(5), 304-310.

> **Reference:** Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. University of California, Irvine. https://archive.ics.uci.edu/

### 3.2 Dataset Limitations

- **Sample size**: Only 303 records (Cleveland database)
- **Demographic bias**: Primarily from a single medical center
- **Temporal bias**: Data collected in the 1980s
- **Missing values**: Some records contain missing `ca` and `thal` values

---

## 4. Data Visualization in Healthcare

### 4.1 Role of Business Intelligence Tools

Business intelligence (BI) tools like Tableau have transformed healthcare analytics by enabling:

- **Interactive exploration** of complex medical datasets
- **Real-time dashboards** for hospital performance monitoring
- **Pattern recognition** across patient populations
- **Story-driven presentations** for non-technical decision makers

> **Reference:** Raghupathi, W., & Raghupathi, V. (2014). *Big data analytics in healthcare: promise and potential*. Health Information Science and Systems, 2(1), 3.

### 4.2 Tableau in Healthcare Research

Several studies have demonstrated the effectiveness of Tableau for healthcare analytics:

1. **Patient Risk Stratification**: Interactive visualizations help clinicians identify high-risk patient groups based on multiple parameters simultaneously.

2. **Epidemiological Dashboards**: Public health agencies use Tableau dashboards for disease surveillance and outbreak monitoring.

3. **Clinical Decision Support**: Embedded analytics in hospital systems provide real-time insights at the point of care.

> **Reference:** Simpao, A. F., et al. (2014). *A review of analytics and clinical informatics in health care*. Journal of Medical Systems, 38(4), 45.

---

## 5. Related Work

### 5.1 Heart Disease Prediction Studies

| Study | Method | Dataset | Key Finding |
|-------|--------|---------|-------------|
| Detrano et al. (1989) | Logistic Regression | Cleveland | 77% accuracy in CAD prediction |
| Aha & Kibler (1988) | Instance-based Learning | Cleveland | Nearest-neighbor approaches effective for diagnosis |
| Janosi et al. (1988) | Various ML methods | Hungarian | Cross-center validation challenges |
| Mohan et al. (2019) | Hybrid Random Forest | Cleveland | 88.7% accuracy with feature selection |
| Ishaq et al. (2021) | Ensemble Methods | Multiple | Gradient Boosting achieved 91.4% accuracy |

### 5.2 Data Visualization Studies in Healthcare

| Study | Focus | Tool | Contribution |
|-------|-------|------|-------------|
| West et al. (2015) | Clinical dashboards | Tableau | Improved ICU monitoring |
| Dowding et al. (2015) | Nursing dashboards | Various | Enhanced clinical decision-making |
| Hauskrecht et al. (2013) | Anomaly detection | Custom | Real-time patient monitoring |

---

## 6. Social and Business Impact

### 6.1 Social Impact

- **Early Detection**: Data-driven analysis enables identification of at-risk individuals before symptom onset
- **Health Awareness**: Interactive dashboards make complex medical data accessible to the general public
- **Preventive Care**: Insights from data analysis support preventive health programs
- **Health Equity**: Demographic analysis highlights disparities in heart disease prevalence

### 6.2 Business Impact

- **Cost Reduction**: Preventive interventions are significantly cheaper than emergency treatments
- **Hospital Efficiency**: Data-driven resource allocation based on patient risk profiles
- **Insurance**: Better risk assessment models for healthcare insurance providers
- **Pharmaceutical**: Targeted drug development based on identified risk factor patterns
- **Policy**: Evidence-based health policy formulation

---

## 7. Conclusion

The literature review establishes that:

1. Heart disease is a critical global health challenge requiring data-driven solutions
2. The UCI Cleveland dataset, despite its limitations, remains a benchmark for heart disease analysis
3. Tableau and other BI tools are increasingly vital for healthcare analytics
4. Interactive visualizations improve both clinical decision-making and public health policy
5. Web integration of dashboards extends the reach and impact of analytical insights

This project builds upon these foundations by combining database management, data preparation, Tableau visualization, and Flask web integration into a comprehensive heart disease analysis solution.

---

## References

1. World Health Organization. (2023). *Cardiovascular Diseases (CVDs) Fact Sheet*. WHO.
2. American Heart Association. (2023). *Understanding Your Risks to Prevent a Heart Attack*. AHA.
3. Detrano, R., et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease*. American Journal of Cardiology, 64(5), 304-310.
4. Dua, D. and Graff, C. (2019). UCI Machine Learning Repository. University of California, Irvine.
5. Raghupathi, W., & Raghupathi, V. (2014). *Big data analytics in healthcare: promise and potential*. Health Information Science and Systems, 2(1), 3.
6. Simpao, A. F., et al. (2014). *A review of analytics and clinical informatics in health care*. Journal of Medical Systems, 38(4), 45.
7. Mohan, S., et al. (2019). *Effective heart disease prediction using hybrid machine learning techniques*. IEEE Access, 7, 81542-81554.
8. Ishaq, A., et al. (2021). *Improving the prediction of heart failure patients' survival using SMOTE and effective data mining techniques*. IEEE Access, 9, 39707-39716.
