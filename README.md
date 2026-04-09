# DataLens : Customer Analytics SaaS Dashboard

A full stack no code analytics platform that lets non technical users upload customer CSV data and instantly get visual insights and automated campaign recommendations.

**Live Demo:** [customer-dashboard-mu-ten.vercel.app](https://customer-dashboard-mu-ten.vercel.app/)
(use the uploaded csv file for the demo)

---

## What It Does

Upload any customer CSV and get back:

- **Revenue breakdown** by product category (bar chart)
- **Age group distribution** across your customer base (pie chart)
- **Top 10 customers** by spend (sortable table)
- **Automated campaign recommendations** priority tagged segments with suggested actions (email campaigns, LINE targeting, re engagement drips)

No configuration. No code. Drop the file, click Analyze.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vue.js 3, ECharts, Axios |
| Backend | FastAPI, Pandas, NumPy |
| Deployment | Vercel (frontend), Render (backend) |
| Data Format | CSV ingestion via multipart upload |

---

## Project Structure

```
customer-dashboard/
│
├── backend/
│   ├── main.py           # FastAPI app — CSV ingestion, analytics, recommendations
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── App.vue
        ├── main.js
        └── components/
            ├── UploadSection.vue         # CSV drag-and-drop upload
            ├── SummaryCards.vue          # KPI cards (revenue, customers, avg spend)
            ├── ChartsSection.vue         # ECharts bar + pie + data table
            └── RecommendationsSection.vue # Priority tagged campaign cards
```

---

## Running Locally

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

**Sample CSV format:**
```
make sure columns have the same headers for now (will be fixed in the future with a ml based matcher)
name,age,category,spend
Alice Chen,28,Electronics,8200
Bob Tanaka,35,Fashion,3400
```

The backend auto detects column names. Any CSV with numeric and categorical columns with mentioned predefined labels will work.

---

## How Recommendations Work (Current)

The current recommendation engine is **rule-based**:

1. Highest revenue category → loyalty email campaign
2. Highest average-spend age group → personalized LINE targeting  
3. Bottom 25% spenders → re-engagement drip campaign

This is fast and interpretable, but the rules are hand-written. See the roadmap below for the ML upgrade path.

---

## Roadmap : ML Integration

The current system uses fixed rules to generate recommendations. The next version replaces this with data driven models that discover patterns automatically.

### Phase 1 : Unsupervised Segmentation (K-Means Clustering)

**What changes:** Instead of manually defining  "top spenders" and "low spenders" or dividing the data based on columns, K-Means automatically discovers natural customer groupings from the data.

**Why it's better:** The model finds segments you wouldn't think to define manually — e.g., "young high-frequency low-spend buyers" vs "older low-frequency high-spend buyers."

**Implementation plan:**
- Encode categorical columns with `pd.get_dummies`
- Normalize features with `StandardScaler`
- Run `KMeans(n_clusters=3)` on age + spend + category features
- Replace hardcoded recommendation segments with cluster-derived segments
- Surface cluster profiles in the frontend (avg spend, age, dominant category per cluster)

---

### Phase 2 — Propensity Scoring (Random Forest Classifier)

**What changes:** The system predicts which customers have the highest probability of converting on a campaign, rather than targeting by spend rank alone.

**Why it's better:** A customer who spent $3,000 twice in 30 days is a better target than someone who spent $5,000 once two years ago. A classifier captures this; a spend threshold doesn't.

 Only meaningful when you have historical campaign outcome data so that the model can be trained using labelled data. So we would need temporal data for this, one off csvs wouldn't create meaningful results.



