# Tableau Visualization Guide: Heart Disease Analysis

## Table of Contents
1. [Connecting Data to Tableau](#1-connecting-data-to-tableau)
2. [Visualizations (10 Unique Charts)](#2-visualizations)
3. [Dashboard Design](#3-dashboard-design)
4. [Story Creation](#4-story-creation)
5. [Calculated Fields Reference](#5-calculated-fields)
6. [Filters Reference](#6-filters)

---

## 1. Connecting Data to Tableau

### Option A: Connect via CSV (Recommended for Tableau Public)
1. Open **Tableau Public** (or Tableau Desktop)
2. Click **Connect → Text file**
3. Navigate to `data/heart_cleaned.csv`
4. Tableau will auto-detect data types

### Option B: Connect via SQLite Database
1. Click **Connect → More... → SQLite**
2. Navigate to `database/heart_disease.db`
3. Select the `heart_disease` table
4. This shows the DB → Tableau connectivity

### Data Source Configuration
After connecting, verify these settings in the Data Source tab:
- `age` → **Number (Whole)**
- `sex` → **Number (Whole)** (will use `sex_label` for display)
- `chol` → **Number (Whole)**
- `trestbps` → **Number (Whole)**
- `thalach` → **Number (Whole)**
- `oldpeak` → **Number (Decimal)**
- `target` → **Number (Whole)**
- All `*_label` columns → **String**
- `risk_score` → **Number (Whole)**

---

## 2. Visualizations

### Visualization 1: Heart Disease Count by Gender (Bar Chart)

**Purpose:** Show the distribution of heart disease across genders.

| Setting | Value |
|---------|-------|
| **Chart Type** | Side-by-side Bar Chart |
| **Columns** | `sex_label` |
| **Rows** | `COUNT(*)` (Number of Records) |
| **Color** | `diagnosis` |
| **Labels** | Show values on bars |

**Steps:**
1. Drag `sex_label` to **Columns**
2. Drag `Number of Records` to **Rows**
3. Drag `diagnosis` to **Color** (on Marks card)
4. Right-click bar → **Show Mark Labels**
5. Title: "Heart Disease Distribution by Gender"

---

### Visualization 2: Chest Pain Type vs Disease (Stacked Bar Chart)

**Purpose:** Analyze which chest pain types are most associated with heart disease.

| Setting | Value |
|---------|-------|
| **Chart Type** | Stacked Bar Chart |
| **Columns** | `cp_label` |
| **Rows** | `COUNT(*)` |
| **Color** | `diagnosis` |
| **Sort** | By count descending |

**Steps:**
1. Drag `cp_label` to **Columns**
2. Drag `Number of Records` to **Rows**
3. Drag `diagnosis` to **Color**
4. Click the **Stacked Bar** icon in the Marks card
5. Title: "Chest Pain Type vs Heart Disease Diagnosis"

---

### Visualization 3: Age Distribution (Histogram)

**Purpose:** Show the age distribution of patients in the dataset.

| Setting | Value |
|---------|-------|
| **Chart Type** | Histogram |
| **Columns** | `age` (binned) |
| **Rows** | `COUNT(*)` |
| **Color** | `diagnosis` |
| **Bin Size** | 5 years |

**Steps:**
1. Right-click `age` → **Create → Bins** → Set bin size to **5**
2. Drag `age (bin)` to **Columns**
3. Drag `Number of Records` to **Rows**
4. Drag `diagnosis` to **Color**
5. Title: "Patient Age Distribution"

---

### Visualization 4: Cholesterol by Disease Status (Box Plot)

**Purpose:** Compare cholesterol levels between patients with and without heart disease.

| Setting | Value |
|---------|-------|
| **Chart Type** | Box-and-Whisker Plot |
| **Columns** | `diagnosis` |
| **Rows** | `chol` |
| **Detail** | Individual data points |

**Steps:**
1. Drag `diagnosis` to **Columns**
2. Drag `chol` to **Rows**
3. Click **Show Me** → Select **Box-and-Whisker Plot**
4. Customize colors for Disease vs No Disease
5. Title: "Cholesterol Levels by Disease Status"

---

### Visualization 5: Max Heart Rate vs Age (Scatter Plot)

**Purpose:** Visualize the relationship between age and maximum heart rate, colored by disease status.

| Setting | Value |
|---------|-------|
| **Chart Type** | Scatter Plot |
| **Columns** | `age` |
| **Rows** | `thalach` |
| **Color** | `diagnosis` |
| **Size** | Fixed or by `risk_score` |
| **Trend Line** | Linear |

**Steps:**
1. Drag `age` to **Columns**
2. Drag `thalach` to **Rows**
3. Change mark type to **Circle**
4. Drag `diagnosis` to **Color**
5. Right-click the chart → **Trend Lines → Show Trend Lines**
6. Title: "Maximum Heart Rate vs Age"

---

### Visualization 6: Correlation Heat Map

**Purpose:** Show correlations between numeric variables.

| Setting | Value |
|---------|-------|
| **Chart Type** | Heat Map / Highlight Table |
| **Approach** | Use calculated fields for correlation |

**Steps:**
1. Create a new sheet
2. For a simpler approach, create a **Highlight Table**:
   - Drag `age_group` to **Rows**
   - Drag `cholesterol_category` to **Columns**
   - Drag `COUNT(*)` to **Color** and **Text**
   - Use a Red-Green diverging color palette
3. Title: "Risk Factor Correlation Matrix"

**Alternative:** Use the `risk_score` vs multiple dimensions to create a multi-variable heat map.

---

### Visualization 7: Disease by Age Group (Donut Chart)

**Purpose:** Show the proportion of heart disease in each age group.

| Setting | Value |
|---------|-------|
| **Chart Type** | Donut Chart (Pie + Circle) |
| **Angle** | `COUNT(*)` |
| **Color** | `age_group` |
| **Filter** | `diagnosis = "Heart Disease"` |

**Steps:**
1. Drag `age_group` to **Color**
2. Drag `Number of Records` to **Angle** (Marks card)
3. Change mark type to **Pie**
4. For donut effect: create a dual axis with a white circle in the center
5. Add labels showing percentage
6. Title: "Heart Disease Proportion by Age Group"

---

### Visualization 8: Cholesterol Trends by Age Group (Line Chart)

**Purpose:** Track average cholesterol across age groups.

| Setting | Value |
|---------|-------|
| **Chart Type** | Line Chart |
| **Columns** | `age_group` |
| **Rows** | `AVG(chol)` |
| **Color** | `diagnosis` |
| **Label** | Show average values |

**Steps:**
1. Drag `age_group` to **Columns**
2. Drag `chol` to **Rows** → Change to **Average**
3. Change mark type to **Line**
4. Drag `diagnosis` to **Color**
5. Add reference line for overall average
6. Title: "Average Cholesterol Trend Across Age Groups"

---

### Visualization 9: Risk Factor Contribution (Tree Map)

**Purpose:** Visualize the relative contribution of different risk levels.

| Setting | Value |
|---------|-------|
| **Chart Type** | Tree Map |
| **Size** | `COUNT(*)` |
| **Color** | `risk_level` |
| **Label** | `risk_level`, count, percentage |

**Steps:**
1. Click **Show Me** → Select **Treemap**
2. Drag `risk_level` to **Color** and **Label**
3. Drag `Number of Records` to **Size**
4. Add percentage calculation to labels
5. Use a Red-Yellow-Green color scheme (Very High = Dark Red, Low = Green)
6. Title: "Patient Risk Level Distribution"

---

### Visualization 10: Blood Pressure Benchmarks (Bullet/Bar Chart)

**Purpose:** Compare patient blood pressure against healthy benchmarks.

| Setting | Value |
|---------|-------|
| **Chart Type** | Grouped Bar Chart |
| **Columns** | `bp_category` |
| **Rows** | `COUNT(*)` |
| **Color** | `diagnosis` |
| **Reference Lines** | AHA benchmark thresholds |

**Steps:**
1. Drag `bp_category` to **Columns**
2. Drag `Number of Records` to **Rows**
3. Drag `diagnosis` to **Color**
4. Add reference lines at 120, 130, 140 mm Hg thresholds
5. Use conditional color formatting
6. Title: "Blood Pressure Categories vs Heart Disease"

---

## 3. Dashboard Design

### Layout
Create a new Dashboard (Dashboard → New Dashboard)

**Size:** Automatic or Fixed (1200 × 800 pixels)

### Recommended Layout:

```
┌────────────────────────────────────────────────────────┐
│                    TITLE / HEADER                       │
│         "Heart Disease Analysis Dashboard"              │
├──────────┬─────────────────────────────────────────────┤
│          │                                              │
│  KPI     │     Viz 1: Gender Bar     │  Viz 2: CP Bar  │
│  Cards   │                           │                  │
│          ├───────────────────────────┼──────────────────┤
│ •Total   │                           │                  │
│ •Rate%   │  Viz 5: Scatter Plot      │  Viz 9: TreeMap  │
│ •AvgChol │                           │                  │
│ •AvgBP   ├───────────────────────────┴──────────────────┤
│          │                                              │
│ FILTERS  │         Viz 8: Line Chart                    │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

### KPI Cards (Calculated Fields)
Create these as separate sheets with BAN (Big-Ass Number) formatting:

1. **Total Patients**: `COUNT([Number of Records])`
2. **Disease Rate**: `SUM(IF [target]=1 THEN 1 ELSE 0 END) / COUNT([Number of Records])`
3. **Avg Cholesterol**: `AVG([chol])`
4. **Avg Blood Pressure**: `AVG([trestbps])`

### Interactive Filters
Add these as dashboard filters (right-click sheet → Filters → Apply to All Worksheets):

1. **Age Group** — Dropdown/Multi-select
2. **Gender** — Radio button (sex_label)
3. **Chest Pain Type** — Dropdown (cp_label)
4. **Risk Level** — Multi-select (risk_level)

### Filter Actions
Add dashboard filter actions:
- Click on gender bar → filters scatter plot, tree map, line chart
- Click on age group → filters all other visualizations

---

## 4. Story Creation

Create a new Story (Story → New Story)

### Scene 1: "The Heart Disease Landscape"
**Caption:** *Understanding the Scale and Demographics of Heart Disease*

Include:
- Dashboard showing overall statistics
- Gender distribution bar chart
- Age distribution histogram
- Annotate key findings (e.g., "Males account for 68% of disease cases")

### Scene 2: "Key Risk Factors Unveiled"
**Caption:** *Deep Diving into Cholesterol, Blood Pressure, and Exercise Patterns*

Include:
- Cholesterol box plot (Viz 4)
- Blood pressure benchmark chart (Viz 10)
- Scatter plot of Heart Rate vs Age (Viz 5)
- Annotate: "Patients with cholesterol >240 have 2x higher disease rate"

### Scene 3: "Actionable Insights for Prevention"
**Caption:** *Data-Driven Recommendations for Healthcare Stakeholders*

Include:
- Risk factor tree map (Viz 9)
- Cholesterol trend line chart (Viz 8)
- Text annotations with recommendations:
  - **For Dr. Sharma:** Focus screening on males aged 50-59 with asymptomatic chest pain
  - **For Ramesh:** Promote cholesterol management programs in 40-60 age group
  - **For Anita:** Monitor cholesterol and exercise habits; maintain heart rate above 150 during exercise

---

## 5. Calculated Fields Reference

Create these calculated fields in Tableau:

| Field Name | Formula |
|-----------|---------|
| Disease Rate | `SUM(IF [target]=1 THEN 1 ELSE 0 END) / COUNT([Number of Records])` |
| Disease Count | `SUM(IF [target]=1 THEN 1 ELSE 0 END)` |
| No Disease Count | `SUM(IF [target]=0 THEN 1 ELSE 0 END)` |
| Age Bin 10 | `INT([age]/10)*10` |
| Chol Risk Flag | `IF [chol] >= 240 THEN "High" ELSEIF [chol] >= 200 THEN "Borderline" ELSE "Normal" END` |
| BP Risk Flag | `IF [trestbps] >= 140 THEN "High" ELSEIF [trestbps] >= 130 THEN "Elevated" ELSE "Normal" END` |
| Heart Rate Zone | `IF [thalach] >= 150 THEN "High" ELSEIF [thalach] >= 100 THEN "Moderate" ELSE "Low" END` |

---

## 6. Filters Reference

| Filter | Field | Type | Applied To |
|--------|-------|------|-----------|
| Age Group | `age_group` | Multi-select | All worksheets |
| Gender | `sex_label` | Single value | All worksheets |
| Chest Pain | `cp_label` | Multi-select | All worksheets |
| Risk Level | `risk_level` | Multi-select | All worksheets |
| Diagnosis | `diagnosis` | Single value | Selected worksheets |
| Cholesterol Range | `chol` | Range slider | Selected worksheets |

---

## Publishing to Tableau Public

1. In Tableau Desktop: **Server → Tableau Public → Save to Tableau Public**
2. Sign in to your Tableau Public account
3. Name your workbook: "Heart Disease Analysis"
4. After publishing, copy the embed URL for the Flask web app
5. The URL format will be: `https://public.tableau.com/views/YourWorkbook/YourDashboard`
