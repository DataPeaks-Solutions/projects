# Healthcare Claims Analytics Using SQL

**DataPeaks Solutions | CDA Series 7 Applied Projects — SQL Track, Project 2**

An end-to-end SQL analysis of 40,000 healthcare claims, uncovering denial patterns, high-risk providers, and payer payout trends using joins, window functions, CASE logic, CTEs, and aggregate filtering.

## 📊 Dataset

- **40,000** claims
- **150** providers
- **8** payers

## 🔍 Key Analysis Covered

- Understanding the healthcare claims data schema
- Denial rates by payer & specialty (`JOIN`s)
- Top providers ranked by billing (window functions)
- High-risk claims flagged by cost + status (`CASE WHEN`)
- Running payer payouts over time (`CTE`s + window functions)
- Outlier providers with abnormal denial volume (`GROUP BY` + `HAVING`)

## 🛠️ Tools

- MySQL Workbench
- SQL (joins, window functions, CTEs, aggregate filtering)

## 📁 Files

| File | Description |
|---|---|
| `analysis.sql` | Full query set — schema setup + all 6 core analyses |
| `data/` | Raw claims, providers, and payers datasets (CSV) |

## ▶️ How to Run

1. Open MySQL Workbench and create a new schema: `datapeaks_healthcare_claims`
2. Import the CSVs in `data/` using Table Data Import Wizard (create `providers`, `payers`, `claims` tables first)
3. Open `analysis.sql` and run each section top to bottom

## 🎥 Video Walkthrough

15-clip SQL deep-dive covering the full analysis: *[https://youtu.be/FKXBy9tJan8]*

## 🔗 About

Part of the **DataPeaks Solutions** CDA Applied Projects series — real-world SQL projects across e-commerce, healthcare, and pharma domains.

- YouTube: [@DatapeaksSolutions](https://youtube.com/@DatapeaksSolutions)
- Instagram: [@datapeaks_solutions](https://instagram.com/datapeaks_solutions)
- GitHub: [DataPeaks-Solutions](https://github.com/DataPeaks-Solutions)
