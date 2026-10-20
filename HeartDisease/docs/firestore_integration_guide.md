# HeartInsight — Cloud Firestore Integration Guide

This guide provides the complete, step-by-step process for connecting the HeartInsight platform with Google Cloud Firestore (using the **Firebase Spark Free Plan** — no credit card or paid Blaze plan required).

---

## 1. Overview of Cloud Architecture

```
┌──────────────────────────────────────┐
│       Local Pipeline / Webapp        │
│    (Python, DuckDB, Parquet, CSV)    │
└──────────────────┬───────────────────┘
                   │
                   ▼  python -m pipeline.firebase_export
┌──────────────────────────────────────┐
│       Google Cloud Firestore         │
│  ├── /analytics/summary              │  <- Aggregated KPIs (Disease rate, Avg BP, Chol)
│  ├── /analytics/duckdb_queries       │  <- 8 Vectorized analytical query caches
│  └── /benchmarks/catalog             │  <- Catalog of 6 multi-center benchmark cohorts
└──────────────────────────────────────┘
```

---

## 2. Step-by-Step Setup Process

### Step 1: Create a Free Firebase Project
1. Open the [Firebase Console](https://console.firebase.google.com/) in your browser.
2. Sign in with your Google account.
3. Click **"Add project"** (or **"Create a project"**).
4. Enter your Project Name: e.g. `heartinsight-platform`.
5. Google Analytics can be toggled **Off** (optional) and click **Create project**.
6. Firebase will initialize your project on the free **Spark plan** ($0/month).

---

### Step 2: Enable Cloud Firestore
1. In the left navigation menu of the Firebase Console, navigate to **Build** → **Firestore Database**.
2. Click **"Create database"**.
3. Choose your database location (select a multi-region or region closest to you, e.g., `asia-south1` or `us-central1`).
4. Under Secure Rules, select **"Start in test mode"** (or production mode; our custom rules in `firestore.rules` will be deployed next).
5. Click **Create** to initialize your Firestore database.

---

### Step 3: Generate the Service Account Key
To allow our Python pipeline to write to Firestore securely:
1. In the Firebase Console, click the **Gear icon (⚙️)** next to "Project Overview" in the top-left corner and select **Project settings**.
2. Select the **Service accounts** tab.
3. Click the blue button labeled **"Generate new private key"**.
4. Confirm by clicking **"Generate key"**.
5. A JSON credentials file will download to your computer.

---

### Step 4: Place the Credentials in the Project
1. Rename the downloaded JSON file to:
   ```
   firebase_credentials.json
   ```
2. Move this file directly into your project root directory:
   ```
   c:\Users\MOHAN VENKAT\OneDrive\Pictures\Desktop\my files\PROJECTS\HeartDisease\firebase_credentials.json
   ```
3. *Security Note:* `.gitignore` is already configured to prevent this key from ever being committed to GitHub.

Alternatively, you can set the environment variable:
```powershell
$env:FIREBASE_SERVICE_ACCOUNT_KEY = "C:\path\to\your-key.json"
```

---

### Step 5: Install the Firebase Admin SDK
Make sure the Firebase SDK is installed in your Python environment:
```powershell
pip install firebase-admin
```

---

### Step 6: Deploy Firestore Security Rules
Deploy the project's security rules using the Firebase CLI:
```powershell
npm install -g firebase-tools
firebase login
firebase deploy --only firestore:rules
```

Our provided [`firestore.rules`](file:///c:/Users/MOHAN%20VENKAT/OneDrive/Pictures/Desktop/my%20files/PROJECTS/HeartDisease/firestore.rules) ensures that:
- Aggregated health metrics and benchmarks are publicly readable by client dashboards.
- Only authenticated pipeline service accounts can write or update data.

---

### Step 7: Run the Firestore Sync
Execute the sync script from your terminal:
```powershell
python -m pipeline.firebase_export
```

**Expected Terminal Output:**
```
[ANALYTICS] Running 8 analytical queries on DuckDB...
[ANALYTICS]    [OK] All 8 queries completed successfully
=================================================================
  [HeartInsight] -- Firebase Firestore Exporter
=================================================================
  Payload assembled: 2 collections
  Local JSON export: .../pipeline/logs/firestore_sync_payload.json
  [OK] Firestore Cloud Upload: SUCCESS (All documents updated)
=================================================================
```

---

## 3. Verify in Firestore Console
1. Return to the [Firebase Console](https://console.firebase.google.com/) → **Firestore Database**.
2. Under the **Data** tab, you will see your collections:
   - `analytics/summary`:
     - `total_patients`: 232 (or 303)
     - `disease_rate_pct`: 48.7%
     - `avg_blood_pressure_mm_hg`: 131.2
     - `avg_cholesterol_mg_dl`: 252.6
     - `data_quality_score`: 98.1%
     - `pipeline_status`: "success"
   - `analytics/duckdb_queries`:
     - All 8 vectorized query outputs cached in real-time.
   - `benchmarks/catalog`:
     - List of all 6 clinical benchmark cohorts.
