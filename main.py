from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

# Enable CORS so Vercel can fetch data from Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load CSV on startup
df = pd.read_csv("colleges_master.csv")

@app.get("/api/predict")
def predict_colleges(
    district: str = "All Districts",
    college_type: str = "All Types (Govt & Private)",
    category: str = "SC",
    percentage: float = 78.0,
    branch: str = "All Branches"
):
    # 1. Filter by Percentage Cutoff
    filtered = df[df["Min Percentage (%)"] <= percentage].copy()

    # 2. Filter by College Type
    if college_type != "All Types (Govt & Private)":
        if "Government" in college_type:
            filtered = filtered[filtered["Type"].str.contains("Government", case=False, na=False)]
        elif "Private" in college_type:
            filtered = filtered[filtered["Type"].str.contains("Private", case=False, na=False)]

    # 3. Filter by Category
    cat_filtered = filtered[filtered["Category"] == category]
    if cat_filtered.empty and category != "OPEN":
        cat_filtered = filtered[filtered["Category"] == "OPEN"]
    filtered = cat_filtered

    # 4. Filter by District & Branch
    if district != "All Districts":
        filtered = filtered[filtered["District"] == district]
    if branch != "All Branches":
        filtered = filtered[filtered["Branch"] == branch]

    # Convert DataFrame results into a JSON list
    return filtered.to_dict(orient="records")