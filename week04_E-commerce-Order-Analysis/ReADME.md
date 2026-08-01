# CDA SQL Track — Project 4: E-commerce Order Analysis

> DataPeaks Solutions | Applied Projects series | SQL deep-dive with a real (synthetic) dataset

One product category cancels and gets returned at almost **double** the rate of every other category in the store. This project builds the dataset from scratch, then writes 10 SQL queries — JOINs, CTEs, window functions, CASE, HAVING — to find out exactly where, and why.

📺 **Watch the full breakdown:** _[https://youtu.be/HvRgnjl4PrQ?si=H1U0s3M4SRqiEawF]_
🌐 **More projects:** [datapeakssolutions.com](https://datapeakssolutions.com)

---

## The dataset

| Table | Rows | Notes |
|---|---|---|
| `customers` | 700 | segment = New / Regular / VIP, 12 Indian cities |
| `products` | 60 | 5 categories, cost + price |
| `orders` | 1,826 | status = Delivered / Cancelled / Returned |
| `order_items` | 4,613 | includes a discount_pct field, some NULLs by design |

Generated with a seeded Python script (`dataset/scripts/generate_data.py`, Faker + `random.seed(42)`) — fully reproducible, and deliberately engineered with real-world patterns rather than pure noise.

## What the queries found

- **Fashion cancels/returns at 35.6%** — every other category sits at 20–22%
- **Lucknow and Nagpur** run 10+ points above every other city on bad-order rate
- **121 VIP customers** (17% of the base) generate **₹2.41 Cr** — nearly matching **423 Regular customers** (60% of the base) at **₹2.40 Cr**
- **Festive-season (Nov–Dec) discounting** drops gross margin from **35.4% to 29.9%**
- **58.1% repeat-purchase rate**; 67 customers signed up and never ordered
- **Total net revenue** (delivered orders only): **₹4.93 Cr**

All figures verified against the actual generated data — see `dataset/README.md` for the full validation.


## Techniques covered

`JOIN` · `LEFT JOIN` · `CTE (WITH)` · `CASE WHEN` · `GROUP BY` / `HAVING` · Window functions: `RANK() OVER`, `ROW_NUMBER() OVER (PARTITION BY ...)`, `LAG() OVER`, `SUM(...) OVER ()`

## Part of the CDA SQL Track

This is Project 4 of DataPeaks Solutions' Applied Projects companion series.
