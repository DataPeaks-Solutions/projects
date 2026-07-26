# Loan Default / Credit Risk Prediction

**DataPeaks Solutions | Series 7 — Python Track, Project 3**
Full Python analysis: `numpy` → `pandas` → `matplotlib` → `scikit-learn`

## What this is

An end-to-end credit risk pipeline on a synthetic loan-applicant dataset:
clean the data, engineer risk features, visualize the drivers of default,
and train two classifiers to predict whether an applicant will default.

## Files

| File | Description |
|---|---|
| `loan_data.csv` | 2,015 synthetic loan applications, 20.4% default rate |
| `analysis.py` | Full pipeline — cleaning, EDA, feature engineering, modeling, evaluation |

## Dataset columns

`age`, `annual_income`, `employment_years`, `credit_score`, `loan_amount`,
`loan_term_months`, `existing_debt`, `num_credit_lines`, `loan_purpose`,
`home_ownership`, `debt_to_income`, `default` (target: 1 = defaulted)

## Pipeline

1. **Load & inspect** — `pandas.read_csv`, shape, dtypes, nulls
2. **Clean** — drop duplicates, impute missing income/employment with medians
3. **Feature engineering (numpy)** — vectorized debt-to-income, log-income, credit utilization
4. **EDA (matplotlib)** — distributions, correlation heatmap
5. **Preprocessing (sklearn)** — one-hot encoding, train/test split, scaling
6. **Modeling** — Logistic Regression (baseline) vs. Random Forest
7. **Evaluation** — classification report, confusion matrix, ROC-AUC, ROC curve
8. **Interpretation** — top feature importances driving default risk

## Results

| Model | ROC-AUC |
|---|---|
| Logistic Regression | 0.926 |
| Random Forest | 0.897 |

Credit score, loan amount, and debt-to-income ratio are the strongest
predictors of default.

## Run it yourself

```bash
pip install numpy pandas matplotlib scikit-learn
python analysis.py
```

Charts save to `./charts/`.

## About

Part of DataPeaks Solutions' Series 7 project library — new analysis weekly.

- Website: [datapeakssolutions.com](https://datapeakssolutions.com)
- Instagram: [@datapeakssolutions](https://instagram.com/datapeakssolutions)
- YouTube: [@datapeakssolutions](https://youtube.com/@datapeakssolutions)
- GitHub: [DataPeaks-Solutions](https://github.com/DataPeaks-Solutions)
