from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df = pd.read_csv("colleges_master.csv")

@app.get("/api/predict")
def predict_colleges(
    percentage: float = 78.0,
    category: str = "SC",
    college_type: str = "All Types",
    district: str = "All Districts",
    branch: str = "All Branches"
):
    # 1. Filter by Percentage
    filtered = df[df["Min Percentage (%)"] <= percentage].copy()

    # 2. Filter by College Type
    if "All" not in college_type:
        if "Government" in college_type:
            filtered = filtered[filtered["Type"].str.contains("Government", case=False, na=False)]
        elif "Private" in college_type or "Un-Aided" in college_type:
            filtered = filtered[filtered["Type"].str.contains("Private", case=False, na=False)]

    # 3. Filter by Category
    cat_filtered = filtered[filtered["Category"] == category]
    if cat_filtered.empty and category != "OPEN":
        cat_filtered = filtered[filtered["Category"] == "OPEN"]
    filtered = cat_filtered

    # 4. Filter by District & Branch
    if "All" not in district:
        filtered = filtered[filtered["District"].str.lower() == district.lower()]
        
    if "All" not in branch:
        filtered = filtered[filtered["Branch"].str.lower() == branch.lower()]

    # Return list of results
    return filtered.to_dict(orient="records")