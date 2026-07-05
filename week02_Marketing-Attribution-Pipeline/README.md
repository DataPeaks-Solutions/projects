# Week 2: Marketing Attribution & Cost Optimization Engine

**DataPeaks Solutions | CDA Track**

Three raw marketing exports. Zero shared format. This pipeline joins them,
fixes the mess, and answers one question: **which channel actually pays for
itself?**

## The Three Raw Tables

| File               | Columns                                              | The Mess |
|---------------------|-------------------------------------------------------|----------|
| `ad_spend.csv`       | `camp_id, date, spend, platform`                       | Spend is in three currencies ($, €, £), each platform exports dates differently |
| `conversions.csv`    | `click_id, camp_id, cust_id, click_time, converted`    | Duplicate click events (click fraud), missing `converted` flags, `click_time` in three date formats |
| `customers.csv`      | `cust_id, signup_dt, ltv`                              | Lifetime value used as the revenue proxy for converted customers |

## Join Keys

```
ad_spend.camp_id  ──▶  conversions.camp_id
conversions.cust_id ──▶  customers.cust_id
```

Two keys chain three tables together: campaign ID links spend to clicks,
customer ID links clicks to identity.

## Pipeline Steps (`analysis.py`)

1. **Load** all three CSVs.
2. **Diagnose** — null percentages per table, dtypes flagged as `object` where they should be numeric/datetime.
3. **Unify dates** — `pd.to_datetime(..., errors='coerce')` collapses `03/14/2026 9:02`, `2026-03-14T10:15:02`, and `14 Mar 26 03:02` into one format.
4. **Find join keys** — `camp_id` and `cust_id`.
5. **Merge** — `ad_spend.merge(conversions, on='camp_id').merge(customers, on='cust_id')`.
6. **De-duplicate** — sort by `click_time`, `drop_duplicates(subset='click_id', keep='first')` to kill duplicate click fraud.
7. **Normalize currency** — a `rates` dict (`$: 1.0, €: 1.08, £: 1.27`) converts every spend value to `spend_usd`.
8. **Pivot** — `pd.pivot_table(index='platform', columns='month', values=['spend_usd','converted','revenue'], aggfunc='sum')`, then collapsed to a channel-level summary.
9. **Compute CAC & ROAS**
   - `CAC = spend_usd / converted`
   - `ROAS = revenue / spend_usd`
10. **Visualize** — a ROAS-by-channel bar chart saved to `roas_by_channel.png`.

## Running It

```bash
pip install pandas numpy matplotlib
python analysis.py
```

## Sample Output

```
platform  spend_usd  converted  revenue    CAC  ROAS
  google     1630.8          4   1820.0 407.70  1.12
    meta     1801.0          7   2075.0 257.29  1.15
  tiktok      687.7          2    455.0 343.85  0.66
```

Numbers will vary slightly as sample data is extended, but the pipeline logic
is fixed: three messy exports in, one clean CAC/ROAS grid out.

## Related: Instagram "Interview Cracker" Reel

`attribution-pipeline-reel-fixed.zip` contains the matching 12-episode
Remotion reel (`Ep01-Hook` → `Ep12-Outro`) that dramatizes this exact
pipeline for Instagram, using the same table names, join keys, and step
order as `analysis.py` above.
