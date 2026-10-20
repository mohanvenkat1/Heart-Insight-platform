# Problem Statement: Heart Disease Analysis with Tableau

## 1. Business Problem

Heart disease is the **leading cause of death globally**, accounting for approximately **17.9 million deaths annually** (WHO, 2023). Despite significant advances in medical science, the ability to identify at-risk individuals before the onset of critical symptoms remains a challenge. Key contributing factors include:

- **Sedentary lifestyles** and lack of physical activity
- **Poor dietary habits** high in saturated fats and sodium
- **Increasing prevalence of comorbidities** such as diabetes, hypertension, and obesity
- **Limited access to preventive healthcare** in certain demographics

The challenge lies in analyzing large-scale health data—encompassing patient demographics, medical history, lifestyle indicators, and clinical measurements—to extract actionable insights that can support **early detection, prevention, and targeted intervention**.

## 2. Business Requirements

| Requirement | Description |
|------------|-------------|
| **R1** | Analyze demographic patterns (age, gender) in heart disease prevalence |
| **R2** | Identify key clinical risk factors (cholesterol, blood pressure, ECG results) |
| **R3** | Create interactive dashboards for healthcare professionals |
| **R4** | Develop comparative visualizations between disease and non-disease groups |
| **R5** | Build a Tableau Story that communicates findings to non-technical stakeholders |
| **R6** | Integrate dashboards into a web application for broader accessibility |
| **R7** | Provide data-driven recommendations for preventive care strategies |

## 3. Scope

### In Scope
- Analysis of the **UCI Heart Disease (Cleveland) dataset** (303 records, 14 attributes)
- Data cleaning, transformation, and database storage using **Python + SQLite**
- **10+ unique visualizations** in Tableau covering demographics, clinical indicators, and risk factors
- **Responsive Tableau Dashboard** with interactive filters
- **Tableau Story** with a minimum of 3 scenes
- **Flask Web Application** for embedding Tableau dashboards
- **Performance testing** of data rendering and filter utilization

### Out of Scope
- Real-time patient data ingestion
- Machine learning prediction models
- HIPAA-compliant data handling (educational dataset)
- Multi-center dataset analysis beyond the Cleveland dataset

## 4. Success Criteria

1. ✅ All 303 records loaded into SQLite database with verified integrity
2. ✅ Cleaned dataset with mapped labels and derived columns
3. ✅ Minimum 10 unique Tableau visualizations
4. ✅ Responsive Tableau Dashboard with 4+ interactive filters
5. ✅ Tableau Story with 3+ meaningful scenes
6. ✅ Flask web app with embedded dashboards accessible at localhost
7. ✅ Complete project documentation

## 5. Key Stakeholders

| Stakeholder | Role | Interest |
|------------|------|----------|
| Dr. Sharma (Scenario 1) | Cardiologist | Clinical risk factor analysis for middle-aged patients |
| Ramesh (Scenario 2) | Health Policy Analyst | Demographic and regional trend analysis |
| Anita (Scenario 3) | Health-conscious Individual | Personal risk factor monitoring |
| Project Mentor | Evaluator | End-to-end project quality and completeness |
