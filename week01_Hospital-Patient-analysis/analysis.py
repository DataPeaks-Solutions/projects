# ============================================================
# Hospital Patient Data Analysis
# DataPeaks Solutions | datapeakssolutions.com
# Author: Arshiya Kauser | IABAC Certified Data Analyst
# ============================================================

import pandas as pd

# ── STEP 1: LOAD DATA ────────────────────────────────────────
print("=" * 55)
print("  HOSPITAL PATIENT DATA ANALYSIS — DataPeaks Solutions")
print("=" * 55)

df = pd.read_csv("data.csv")
print(f"\n✅ Data Loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ── STEP 2: EXPLORE ──────────────────────────────────────────
print("\n📋 Dataset Preview:")
print(df[["PatientID", "Age", "Department", "Diagnosis", "Status"]].head(5).to_string(index=False))

print(f"\n🔍 Missing Values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# ── STEP 3: CLEAN DATA ───────────────────────────────────────
# Fill missing LOS_Days with median per department
df["LOS_Days"] = pd.to_numeric(df["LOS_Days"], errors="coerce")
df["Bill_Amount"] = pd.to_numeric(df["Bill_Amount"], errors="coerce")

median_los = df.groupby("Department")["LOS_Days"].transform("median")
df["LOS_Days"] = df["LOS_Days"].fillna(median_los)

# Fill missing Bill_Amount with 0 for still-admitted patients
df["Bill_Amount"] = df["Bill_Amount"].fillna(0)

print(f"\n✅ Missing values handled.")

# ── STEP 4: ANALYSE ──────────────────────────────────────────

# 4A: Patient count by Department
print("\n📊 Patients by Department:")
dept_summary = (
    df.groupby("Department")
    .agg(
        Total_Patients=("PatientID", "count"),
        Avg_LOS_Days=("LOS_Days", "mean"),
        Total_Revenue=("Bill_Amount", "sum"),
    )
    .sort_values("Total_Patients", ascending=False)
    .reset_index()
)
dept_summary["Avg_LOS_Days"] = dept_summary["Avg_LOS_Days"].round(1)
dept_summary["Total_Revenue"] = dept_summary["Total_Revenue"].apply(lambda x: f"₹{x:,.0f}")
print(dept_summary.to_string(index=False))

# 4B: Payment mode breakdown
print("\n💳 Payment Mode Breakdown:")
payment_summary = (
    df.groupby("Payment_Mode")["PatientID"]
    .count()
    .reset_index()
    .rename(columns={"PatientID": "Patients"})
    .sort_values("Patients", ascending=False)
)
print(payment_summary.to_string(index=False))

# 4C: Currently admitted patients
print("\n🏥 Currently Admitted Patients:")
admitted = df[df["Status"] == "Admitted"][
    ["PatientID", "Name", "Department", "Diagnosis", "LOS_Days"]
]
print(admitted.to_string(index=False))

# ── STEP 5: SUMMARY ──────────────────────────────────────────
print("\n" + "=" * 55)
print("  FINAL SUMMARY")
print("=" * 55)
print(f"  Total Patients Recorded : {len(df)}")
print(f"  Patients Discharged     : {len(df[df['Status']=='Discharged'])}")
print(f"  Patients Still Admitted : {len(df[df['Status']=='Admitted'])}")
print(f"  Average Age             : {df['Age'].mean():.1f} years")
print(f"  Avg Length of Stay      : {df['LOS_Days'].mean():.1f} days")
print(f"  Total Revenue Generated : ₹{df['Bill_Amount'].sum():,.0f}")
top_dept = dept_summary.iloc[0]["Department"]
print(f"  Busiest Department      : {top_dept}")
print("=" * 55)
print("\n✅ Analysis Complete! | github.com/DataPeaksSolutions")