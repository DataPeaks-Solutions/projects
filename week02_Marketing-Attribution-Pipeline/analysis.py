# ==============================================================================
# MARKETING ATTRIBUTION & COST OPTIMIZATION ENGINE
# DataPeaks Solutions | datapeakssolutions.com
# Week 2 -- CDA Track
# ==============================================================================
#
# Three raw exports, three different shapes, zero shared format:
#   ad_spend.csv     -> camp_id, date,       spend,      platform
#   conversions.csv  -> click_id, camp_id, cust_id, click_time, converted
#   customers.csv    -> cust_id, signup_dt,  ltv
#
# This script joins them on camp_id / cust_id, fixes mixed date formats and
# mixed currencies, drops duplicate click fraud, and rolls everything up into
# CAC (Customer Acquisition Cost) and ROAS (Return on Ad Spend) by platform.
# ==============================================================================

import pandas as pd
import numpy as np

pd.set_option("display.width", 120)

print("=" * 65)
print(" PIPELINE INITIALIZED: THREE TABLES, ZERO CONNECTION")
print("=" * 65)

# ------------------------------------------------------------------
# STEP 1 -- LOAD RAW TABLES  (Ep01: The Hook)
# ------------------------------------------------------------------
ad_spend = pd.read_csv("ad_spend.csv")
conversions = pd.read_csv("conversions.csv")
customers = pd.read_csv("customers.csv")

tables = {"ad_spend": ad_spend, "conversions": conversions, "customers": customers}

for name, df in tables.items():
    print(f"\n[STEP 1] {name}: {df.shape[0]} rows x {df.shape[1]} columns")

# ------------------------------------------------------------------
# STEP 2 -- STRUCTURAL DIAGNOSTICS  (Ep02: Diagnostics)
# ------------------------------------------------------------------
print("\n[STEP 2] Deep Structural Diagnostics:")
for name, df in tables.items():
    nulls_pct = (df.isna().mean() * 100).round(1)
    print(f"\n  {name} null %:")
    print("  " + nulls_pct.to_string().replace("\n", "\n  "))

# ------------------------------------------------------------------
# STEP 3 -- UNIFY UNSTRUCTURED DATE FORMATS  (Ep03: Datetime Parse)
# ------------------------------------------------------------------
# meta   -> 03/14/2026 9:02
# google -> 2026-03-14T10:15:02
# tiktok -> 14 Mar 26 03:02
conversions["click_time"] = pd.to_datetime(conversions["click_time"], errors="coerce")
ad_spend["date"] = pd.to_datetime(ad_spend["date"], errors="coerce")
print("\n[STEP 3] click_time / date formats unified across all platforms.")

# ------------------------------------------------------------------
# STEP 4 -- FIND THE JOIN KEYS  (Ep04: Merge Setup)
# ------------------------------------------------------------------
# camp_id  chains ad_spend      -> conversions
# cust_id  chains conversions   -> customers
print("\n[STEP 4] Join keys: ad_spend.camp_id -> conversions.camp_id -> customers.cust_id")

# ------------------------------------------------------------------
# STEP 5 -- MERGE THE THREE TABLES  (Ep05: Merge Execute)
# ------------------------------------------------------------------
rows_before = len(ad_spend)
merged = ad_spend.merge(
    conversions, on="camp_id", how="left"
).merge(customers, on="cust_id", how="left")
rows_after = len(merged)
print(f"\n[STEP 5] Rows before merge: {rows_before} | Rows after merge: {rows_after}")

# ------------------------------------------------------------------
# STEP 6 -- KILL DUPLICATE CLICK FRAUD  (Ep06: Dedup)
# ------------------------------------------------------------------
merged = merged.sort_values("click_time")
dupes = merged.duplicated(subset="click_id", keep="first").sum()
merged = merged.drop_duplicates(subset="click_id", keep="first")
pct_dupes = round(100 * dupes / rows_after, 1) if rows_after else 0
print(f"\n[STEP 6] Duplicate clicks removed: {dupes} ({pct_dupes}% of merged rows)")

# ------------------------------------------------------------------
# STEP 7 -- ONE CURRENCY TO RULE THEM ALL  (Ep07: Currency Normalize)
# ------------------------------------------------------------------
rates = {"$": 1.0, "\u20ac": 1.08, "\u00a3": 1.27}


def clean_currency(value, rates=rates):
    if isinstance(value, str):
        for symbol, rate in rates.items():
            if symbol in value:
                return round(float(value.replace(symbol, "").strip()) * rate, 2)
    return pd.to_numeric(value, errors="coerce")


merged["spend_usd"] = merged["spend"].apply(clean_currency)
print("\n[STEP 7] Sample normalized spend (raw -> spend_usd):")
print(merged[["spend", "spend_usd"]].drop_duplicates().head(6).to_string(index=False))

# ------------------------------------------------------------------
# STEP 8/9 -- BUILD THE PIVOT ENGINE  (Ep08: Pivot Setup, Ep09: Pivot Execute)
# ------------------------------------------------------------------
merged["converted"] = merged["converted"].fillna(0).astype(int)
merged["revenue"] = np.where(merged["converted"] == 1, merged["ltv"].fillna(0), 0)
merged["month"] = merged["date"].dt.to_period("M").astype(str)

pivot = pd.pivot_table(
    merged,
    index="platform",
    columns="month",
    values=["spend_usd", "converted", "revenue"],
    aggfunc="sum",
).fillna(0)

# Collapse the month columns into one channel-level summary table
summary = merged.groupby("platform").agg(
    spend_usd=("spend_usd", "sum"),
    converted=("converted", "sum"),
    revenue=("revenue", "sum"),
).reset_index()

print("\n[STEP 8/9] Channel-by-month pivot collapsed into a clean grid:")
print(summary.to_string(index=False))

# ------------------------------------------------------------------
# STEP 10 -- THE NUMBERS THAT MATTER: CAC & ROAS  (Ep10: Metrics)
# ------------------------------------------------------------------
summary["CAC"] = np.where(
    summary["converted"] > 0, summary["spend_usd"] / summary["converted"], np.nan
)
summary["ROAS"] = np.where(
    summary["spend_usd"] > 0, summary["revenue"] / summary["spend_usd"], 0
)
summary["CAC"] = summary["CAC"].round(2)
summary["ROAS"] = summary["ROAS"].round(2)

print("\n[STEP 10] CAC & ROAS by channel:")
print(summary[["platform", "spend_usd", "converted", "revenue", "CAC", "ROAS"]].to_string(index=False))

# ------------------------------------------------------------------
# STEP 11 -- VISUALIZE THE WINNER  (Ep11: Visualization)
# ------------------------------------------------------------------
try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(summary["platform"], summary["ROAS"], color=["#00f5ff", "#00ff66", "#ff2a85"])
    ax.set_title("ROAS by Channel")
    ax.set_ylabel("ROAS (x)")
    for i, v in enumerate(summary["ROAS"]):
        ax.text(i, v + 0.05, f"{v}x", ha="center")
    fig.tight_layout()
    fig.savefig("roas_by_channel.png", dpi=150)
    print("\n[STEP 11] Saved roas_by_channel.png")
except ImportError:
    print("\n[STEP 11] matplotlib not installed -- skipped chart export.")

winner = summary.loc[summary["ROAS"].idxmax()]
print(f"\n[STEP 11] Winner: {winner['platform'].upper()} \u2013 {winner['ROAS']}x ROAS")

# ------------------------------------------------------------------
# STEP 12 -- PIPELINE VERIFIED  (Ep12: Outro)
# ------------------------------------------------------------------
print("\n" + "=" * 65)
print(" PIPELINE VERIFIED: Chaos -> Clean -> CAC & ROAS")
print(" Three messy exports, cleaned end-to-end into a real business answer.")
print("=" * 65)
