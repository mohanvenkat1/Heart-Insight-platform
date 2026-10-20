# Performance Testing Report

**Generated:** 2026-10-20 15:02:53

## 1. Data Rendered to Database

| Metric | Value |
|--------|-------|
| Raw CSV Records | 310 |
| Cleaned CSV Records | 232 |
| Database Records | 310 |
| Database File Size | 24.0 KB |
| Table Count | 1 (heart_disease) |
| Columns per Record | 14 |

## 2. Query Performance Benchmarks

| # | Query Description | Rows | Time (ms) |
|---|------------------|------|-----------|
| 1 | Full table scan | 310 | 1.158 |
| 2 | Filter: Disease patients | 121 | 0.606 |
| 3 | Filter: High-risk patients | 41 | 0.208 |
| 4 | Aggregate: By gender | 2 | 0.157 |
| 5 | Aggregate: By age group | 4 | 0.199 |
| 6 | Cross-tab: Gender × ChestPain | 8 | 0.177 |
| 7 | Calculated fields query | 310 | 0.942 |
| 8 | Full sort: Age + Chol | 310 | 0.905 |
| 9 | HAVING clause | 4 | 0.494 |
| 10 | Multi-filter complex | 59 | 0.286 |

**Average Query Time:** 0.513 ms
**Min Query Time:** 0.157 ms
**Max Query Time:** 1.158 ms

## 3. Data Filters Utilization

| # | Filter Name | Field | Type | Scope |
|---|------------|-------|------|-------|
| 1 | Age Group | `age_group` | Multi-select dropdown | All worksheets |
| 2 | Gender | `sex_label` | Radio button (Single value) | All worksheets |
| 3 | Chest Pain Type | `cp_label` | Multi-select dropdown | All worksheets |
| 4 | Risk Level | `risk_level` | Multi-select dropdown | All worksheets |
| 5 | Diagnosis | `diagnosis` | Single value dropdown | Selected worksheets |
| 6 | Cholesterol Range | `chol` | Range slider | Selected worksheets |
| 7 | Blood Pressure Range | `trestbps` | Range slider | Selected worksheets |
| 8 | Age Range | `age` | Range slider | Dashboard only |

**Total Filters:** 8

## 4. Calculated Fields

| # | Field Name | Formula / Description |
|---|-----------|----------------------|
| 1 | Disease Rate | `SUM(IF [target]=1 THEN 1 ELSE 0 END) / COUNT([Records])` |
| 2 | Disease Count | `SUM(IF [target]=1 THEN 1 ELSE 0 END)` |
| 3 | No Disease Count | `SUM(IF [target]=0 THEN 1 ELSE 0 END)` |
| 4 | Age Bin 10 | `INT([age]/10)*10` |
| 5 | Chol Risk Flag | `IF [chol]>=240 THEN 'High' ELSEIF [chol]>=200 THEN 'Borderline' ELSE 'Normal'` |
| 6 | BP Risk Flag | `IF [trestbps]>=140 THEN 'High' ELSEIF [trestbps]>=130 THEN 'Elevated' ELSE 'Normal'` |
| 7 | Heart Rate Zone | `IF [thalach]>=150 THEN 'High' ELSEIF [thalach]>=100 THEN 'Moderate' ELSE 'Low'` |
| 8 | Risk Score | `Composite of age, chol, bp, exang, oldpeak, fbs, ca` |
| 9 | Risk Level | `Based on risk_score: Low/Moderate/High/Very High` |
| 10 | Age Group | `Binned age into 10-year groups` |

**Total Calculated Fields:** 10

## 5. Visualizations / Graphs

| # | Chart Type | Description |
|---|-----------|-------------|
| 1 | Bar Chart | Heart Disease Count by Gender |
| 2 | Stacked Bar | Chest Pain Type vs Disease Presence |
| 3 | Histogram | Age Distribution of Patients |
| 4 | Box Plot | Cholesterol Levels by Disease Status |
| 5 | Scatter Plot | Max Heart Rate vs Age |
| 6 | Heat Map | Risk Factor Correlation Matrix |
| 7 | Donut Chart | Disease Proportion by Age Group |
| 8 | Line Chart | Cholesterol Trends Across Age Groups |
| 9 | Tree Map | Risk Factor Contribution |
| 10 | Grouped Bar | Blood Pressure Benchmarks vs Disease |

**Total Unique Visualizations:** 10

## 6. Performance Summary

| Metric | Count |
|--------|-------|
| Data Records in DB | 310 |
| Database Size | 24.0 KB |
| Total Filters | 8 |
| Total Calculated Fields | 10 |
| Total Visualizations | 10 |
| Dashboard Count | 1 |
| Story Scenes | 3 |

### Verdict: ✅ All performance criteria met