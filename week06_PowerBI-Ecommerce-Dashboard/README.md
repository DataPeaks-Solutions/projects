# E-Commerce Order Analysis Dashboard
**CDA Applied Project · Power BI · DataPeaks Solutions**

A single-page, glassmorphic Power BI dashboard analyzing 700 customers, 1,826 orders, and 4,613 line items from an e-commerce dataset — built as part of the DataPeaks Solutions Certified Data Analyst (CDA) Applied Projects series.

**Live report:** https://app.powerbi.com/links/MV5f1O4X6V?ctid=f1e56b10-5f67-4e70-bd40-8c6948bde6cf&pbi_source=linkShare

---

## Overview

| | |
|---|---|
| **Track** | Certified Data Analyst (CDA) — Power BI |
| **Dataset** | 700 customers · 1,826 orders · 4,613 order items |
| **Layout** | 1 page, 8 visuals |
| **Design system** | Glassmorphic dark-navy (`#020d1a`) / cyan (`#00e5ff`) |
| **Net revenue analyzed** | ₹4.93 Cr |
| **Companion video** | 10-episode walkthrough (on youtube) |

## Key Insights

- **VIP vs Regular customers generate almost exactly the same revenue** (₹2.41 Cr vs ₹2.40 Cr) — a near-parity finding that challenges the assumption that VIP tiers drive disproportionate revenue.
- **Fashion has the highest cancellation rate** among categories, at 35.6%.
- **Lucknow and Nagpur emerge as outlier cities** in the order/city breakdown, outside the expected metro-heavy pattern.

## Dashboard Visuals

1. KPI strip (revenue, orders, customers, AOV)
2. Category-wise order volume (bar)
3. Revenue trend over time (line)
4. City-wise order distribution
5. VIP vs Regular revenue donut comparison
6. Cancellation rate by category
7. Order status breakdown
8. Top customers / order value distribution


## Tech Stack

- **Power BI Desktop** — dashboard build, DAX measures, data modeling
- **MySQL** — source data (`ecommerce_analysis` schema)
- **Remotion + TypeScript + React** — walkthrough video generation
- **ffmpeg / ffprobe** — audio-duration sync and final video stitching

## About DataPeaks Solutions

DataPeaks Solutions is a data analytics training institute based in Hyderabad, offering courses across six tracks: Certified Data Analyst (CDA), CDS, CDE, MLE, GenAI, and Agentic AI.

- Website: [datapeakssolutions.com](https://datapeakssolutions.com)
- YouTube: [@DatapeaksSolutions](https://youtube.com/@DatapeaksSolutions)
- Instagram: [@datapeaks_solutions](https://instagram.com/datapeaks_solutions)
- GitHub: [github.com/DataPeaks-Solutions](https://github.com/DataPeaks-Solutions)

---

*Part of the CDA Applied Projects series — real-world Power BI, SQL, and Python projects built end-to-end for the DataPeaks curriculum.*
