from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import io
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean(obj):
    """Convert all numpy types to plain Python types so FastAPI can serialize them"""
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean(i) for i in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj) if not isinstance(obj, (list, dict, np.ndarray)) else False:
        return None
    return obj

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

    results = {}

    bins = [0, 18, 25, 35, 45, 60, 100]
    labels = ["<18", "18-25", "25-35", "35-45", "45-60", "60+"]

    if "age" in df.columns:
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)
        age_dist = df["age_group"].value_counts().sort_index()
        results["age_distribution"] = {
            "labels": [str(x) for x in age_dist.index.tolist()],
            "values": [int(x) for x in age_dist.values.tolist()]
        }

    spend_col = next((c for c in numeric_cols if any(x in c for x in ["spend","amount","purchase","revenue"])), None)
    cat_col = next((c for c in cat_cols if any(x in c for x in ["category","product","segment","type"])), None)

    if spend_col and cat_col:
        spend_by_cat = df.groupby(cat_col)[spend_col].sum().sort_values(ascending=False).head(8)
        results["spend_by_category"] = {
            "labels": [str(x) for x in spend_by_cat.index.tolist()],
            "values": [round(float(v), 2) for v in spend_by_cat.values.tolist()],
            "category_col": str(cat_col),
            "spend_col": str(spend_col)
        }

    name_col = next((c for c in cat_cols if any(x in c for x in ["name","customer","id"])), None)
    if spend_col and name_col:
        cols = [name_col, spend_col]
        if "age" in df.columns:
            cols = [name_col, "age", spend_col]
        top_customers = df.nlargest(10, spend_col)[cols]
        results["top_customers"] = [
            {k: (int(v) if isinstance(v, np.integer) else float(v) if isinstance(v, np.floating) else str(v))
             for k, v in row.items()}
            for row in top_customers.to_dict(orient="records")
        ]

    results["summary"] = {
        "total_customers": int(len(df)),
        "total_revenue": round(float(df[spend_col].sum()), 2) if spend_col else None,
        "avg_spend": round(float(df[spend_col].mean()), 2) if spend_col else None,
        "columns_detected": [str(c) for c in df.columns.tolist()]
    }

    recommendations = []

    if spend_col and cat_col:
        spend_by_cat = df.groupby(cat_col)[spend_col].sum().sort_values(ascending=False).head(8)
        top_cat = str(spend_by_cat.index[0])
        top_val = round(float(spend_by_cat.values[0]), 2)
        recommendations.append({
            "segment": f"High-value {top_cat} buyers",
            "action": "Send exclusive loyalty email campaign",
            "reason": f"This segment generates the highest revenue: ${top_val:,}. High conversion likelihood.",
            "priority": "HIGH"
        })

    if "age" in df.columns and spend_col:
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)
        best_age = str(df.groupby("age_group")[spend_col].mean().idxmax())
        best_val = round(float(df.groupby("age_group")[spend_col].mean().max()), 2)
        recommendations.append({
            "segment": f"Age group {best_age}",
            "action": "Target with personalized product recommendations via LINE",
            "reason": f"Highest average spend per customer: ${best_val}. Strong ROI on targeted campaigns.",
            "priority": "HIGH"
        })

    if spend_col:
        low_spenders = df[df[spend_col] < df[spend_col].quantile(0.25)]
        recommendations.append({
            "segment": "Low-engagement customers (bottom 25% spend)",
            "action": "Re-engagement drip campaign",
            "reason": f"{int(len(low_spenders))} customers with minimal activity. Win-back opportunity with discount incentive.",
            "priority": "MEDIUM"
        })

    results["recommendations"] = recommendations

    return clean(results)


@app.get("/")
def root():
    return {"status": "Customer Analytics API is running"}