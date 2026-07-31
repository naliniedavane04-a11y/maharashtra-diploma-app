import pandas as pd

branches = [
    "Computer Engineering", "Information Technology", "Artificial Intelligence & Data Science",
    "Electronics & Telecommunication", "Electrical Engineering", "Mechanical Engineering",
    "Civil Engineering", "Chemical Engineering", "Automobile Engineering"
]

categories = ["OPEN", "OBC", "SC", "ST", "EWS", "NT-A", "NT-B", "NT-C", "NT-D", "VJ/DT", "TFWS"]

district_institutes = [
    {"District": "Nagpur", "Name": "Government Polytechnic, Nagpur", "Type": "Government", "Base_OPEN": 84.0, "Base_Fee": 7750, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹4,500 - ₹6,000 / year"},
    {"District": "Nagpur", "Name": "Anjuman Polytechnic, Nagpur", "Type": "Private (Minority)", "Base_OPEN": 68.0, "Base_Fee": 48000, "Hostel": "Yes (Boys Only)", "Hostel_Fee": "₹35,000 / year"},
    {"District": "Nagpur", "Name": "Shri Datta Meghe Polytechnic, Nagpur", "Type": "Private (Un-Aided)", "Base_OPEN": 74.0, "Base_Fee": 58000, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹45,000 / year"},
    {"District": "Nanded", "Name": "Government Polytechnic, Nanded", "Type": "Government", "Base_OPEN": 82.0, "Base_Fee": 7750, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹4,500 / year"},
    {"District": "Nanded", "Name": "Gramin Polytechnic, Vishnupuri, Nanded", "Type": "Private (Un-Aided)", "Base_OPEN": 66.0, "Base_Fee": 45000, "Hostel": "No (Private PG Nearby)", "Hostel_Fee": "₹30,000 / year (PG)"},
    {"District": "Mumbai City", "Name": "Veermata Jijabai Technological Institute (VJTI)", "Type": "Government-Aided", "Base_OPEN": 94.5, "Base_Fee": 11500, "Hostel": "Yes (Limited Merit Seats)", "Hostel_Fee": "₹8,000 - ₹12,000 / year"},
    {"District": "Mumbai Suburban", "Name": "Government Polytechnic, Mumbai", "Type": "Government", "Base_OPEN": 88.0, "Base_Fee": 7750, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹4,500 / year"},
    {"District": "Mumbai Suburban", "Name": "Vivekanand Education Society Polytechnic, Chembur", "Type": "Private (Aided/Un-Aided)", "Base_OPEN": 82.0, "Base_Fee": 65000, "Hostel": "No (Local PG Available)", "Hostel_Fee": "₹60,000 / year (PG)"},
    {"District": "Pune", "Name": "Government Polytechnic, Pune", "Type": "Government", "Base_OPEN": 89.0, "Base_Fee": 7750, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹4,500 / year"},
    {"District": "Pune", "Name": "Cusrow Wadia Institute of Technology, Pune", "Type": "Government-Aided", "Base_OPEN": 84.0, "Base_Fee": 10500, "Hostel": "Yes (In-Campus)", "Hostel_Fee": "₹18,000 / year"},
    {"District": "Pune", "Name": "AISSMS Polytechnic, Pune", "Type": "Private (Un-Aided)", "Base_OPEN": 77.0, "Base_Fee": 68000, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹55,000 / year"},
    {"District": "Chhatrapati Sambhajinagar", "Name": "Government Polytechnic, Chhatrapati Sambhajinagar", "Type": "Government", "Base_OPEN": 83.0, "Base_Fee": 7750, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹4,500 / year"},
    {"District": "Nashik", "Name": "Government Polytechnic, Nashik", "Type": "Government", "Base_OPEN": 81.0, "Base_Fee": 7750, "Hostel": "Yes (Boys & Girls)", "Hostel_Fee": "₹4,500 / year"},
    {"District": "Nashik", "Name": "KK Wagh Polytechnic, Nashik", "Type": "Private (Un-Aided)", "Base_OPEN": 75.0, "Base_Fee": 55000, "Hostel": "Yes (In-Campus)", "Hostel_Fee": "₹40,000 / year"}
]

records = []

for inst in district_institutes:
    base_open = inst["Base_OPEN"]
    base_fee = inst["Base_Fee"]
    
    for br in branches:
        br_mod = 0.0 if "Computer" in br else (-2.0 if "Information" in br or "Artificial" in br else (-6.0 if "Electronics" in br or "Electrical" in br else -8.0))
        
        for cat in categories:
            cat_mod = +5.0 if cat == "TFWS" else (0.0 if cat == "OPEN" else (-2.0 if cat == "EWS" else (-4.0 if cat == "OBC" else (-7.0 if cat in ["NT-A", "NT-B", "NT-C", "NT-D", "VJ/DT"] else (-10.0 if cat == "SC" else -18.0)))))
            final_cutoff = round(max(35.0, min(98.5, base_open + br_mod + cat_mod)), 1)
            
            if cat in ["SC", "ST", "TFWS"]:
                est_fee = "₹1,000 - ₹2,000 / year"
            elif cat in ["OBC", "EWS", "NT-A", "NT-B", "NT-C", "NT-D", "VJ/DT"]:
                est_fee = f"₹{int(base_fee * 0.5):,} / year"
            else:
                est_fee = f"₹{base_fee:,} / year"
            
            records.append({
                "College Name": inst["Name"],
                "District": inst["District"],
                "Type": inst["Type"],
                "Branch": br,
                "Category": cat,
                "Min Percentage (%)": final_cutoff,
                "Approx Annual Fees": est_fee,
                "Hostel Facility": inst["Hostel"],
                "Hostel Fee": inst["Hostel_Fee"]
            })

df = pd.DataFrame(records)
df.to_csv("colleges_master.csv", index=False)
print("SUCCESS: colleges_master.csv created in your project directory!")