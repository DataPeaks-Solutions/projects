"""
analysis.py
Loan Default / Credit Risk Prediction — full pipeline
DataPeaks Solutions | Series 7 — Python Track Project 3

Covers: numpy, pandas, matplotlib, scikit-learn
Run: python analysis.py
Outputs: PNG charts in ./charts/ and console metrics
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)

os.makedirs("charts", exist_ok=True)
plt.rcParams["figure.figsize"] = (8, 5)


# =============================================================================
# CLIP 2 — Load raw CSV with pandas, first look
# =============================================================================
df = pd.read_csv("loan_data.csv")
print("Shape:", df.shape)
print(df.head())
print(df.info())
print(df.isna().sum())


# =============================================================================
# CLIP 3 — Data cleaning: nulls, dtypes, duplicates
# =============================================================================
df = df.drop_duplicates()

df["annual_income"] = df["annual_income"].fillna(df["annual_income"].median())
df["employment_years"] = df["employment_years"].fillna(df["employment_years"].median())

df["loan_purpose"] = df["loan_purpose"].astype("category")
df["home_ownership"] = df["home_ownership"].astype("category")

print("\nAfter cleaning:", df.shape)
print(df.isna().sum().sum(), "missing values remain")


# =============================================================================
# CLIP 4 — numpy: vectorized feature calculations
# =============================================================================
# Recompute debt-to-income cleanly, add a log-scaled income feature and a
# credit utilization proxy — all done with vectorized numpy ops, no loops.
df["debt_to_income"] = np.round(
    (df["existing_debt"] + df["loan_amount"]) / df["annual_income"], 3
)
df["log_income"] = np.log1p(df["annual_income"])
df["credit_utilization"] = np.round(
    df["existing_debt"] / (df["existing_debt"] + df["loan_amount"] + 1), 3
)

print("\nEngineered feature sample:")
print(df[["debt_to_income", "log_income", "credit_utilization"]].describe())


# =============================================================================
# CLIP 5 — EDA: distributions with matplotlib
# =============================================================================
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
axes[0].hist(df["credit_score"], bins=30, color="#2C7FB8", edgecolor="white")
axes[0].set_title("Credit Score Distribution")
axes[0].set_xlabel("Credit Score")

axes[1].hist(df["debt_to_income"], bins=30, color="#D95F0E", edgecolor="white")
axes[1].set_title("Debt-to-Income Distribution")
axes[1].set_xlabel("Debt-to-Income Ratio")
plt.tight_layout()
plt.savefig("charts/01_distributions.png", dpi=150)
plt.close()


# =============================================================================
# CLIP 6 — EDA: correlation heatmap
# =============================================================================
numeric_cols = [
    "age", "annual_income", "employment_years", "credit_score", "loan_amount",
    "existing_debt", "num_credit_lines", "debt_to_income", "credit_utilization",
    "default"
]
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(numeric_cols)))
ax.set_yticks(range(len(numeric_cols)))
ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
ax.set_yticklabels(numeric_cols)
fig.colorbar(im, ax=ax, label="Correlation")
ax.set_title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("charts/02_correlation_heatmap.png", dpi=150)
plt.close()


# =============================================================================
# CLIP 7 — Feature engineering (pandas + numpy combined)
# =============================================================================
df["income_bracket"] = pd.cut(
    df["annual_income"], bins=[0, 30000, 60000, 100000, np.inf],
    labels=["low", "mid", "high", "very_high"]
)
df_model = pd.get_dummies(
    df, columns=["loan_purpose", "home_ownership", "income_bracket"], drop_first=True
)


# =============================================================================
# CLIP 8 — Train/test split, preprocessing (sklearn)
# =============================================================================
feature_cols = [c for c in df_model.columns if c not in ("default",)]
X = df_model[feature_cols]
y = df_model["default"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"\nTrain size: {X_train.shape[0]}  Test size: {X_test.shape[0]}")


# =============================================================================
# CLIP 9 — Model 1: baseline Logistic Regression
# =============================================================================
logreg = LogisticRegression(max_iter=1000, random_state=42)
logreg.fit(X_train_scaled, y_train)
logreg_preds = logreg.predict(X_test_scaled)
logreg_probs = logreg.predict_proba(X_test_scaled)[:, 1]

print("\n--- Logistic Regression ---")
print(classification_report(y_test, logreg_preds))
print("ROC-AUC:", round(roc_auc_score(y_test, logreg_probs), 3))


# =============================================================================
# CLIP 10 — Model 2: Random Forest
# =============================================================================
rf = RandomForestClassifier(
    n_estimators=300, max_depth=8, random_state=42, class_weight="balanced"
)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
rf_probs = rf.predict_proba(X_test)[:, 1]

print("\n--- Random Forest ---")
print(classification_report(y_test, rf_preds))
print("ROC-AUC:", round(roc_auc_score(y_test, rf_probs), 3))


# =============================================================================
# CLIP 11 — Evaluation: confusion matrix + ROC curve
# =============================================================================
cm = confusion_matrix(y_test, rf_preds)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

im = axes[0].imshow(cm, cmap="Blues")
axes[0].set_title("Random Forest — Confusion Matrix")
axes[0].set_xlabel("Predicted")
axes[0].set_ylabel("Actual")
axes[0].set_xticks([0, 1]); axes[0].set_xticklabels(["No Default", "Default"])
axes[0].set_yticks([0, 1]); axes[0].set_yticklabels(["No Default", "Default"])
for i in range(2):
    for j in range(2):
        axes[0].text(j, i, cm[i, j], ha="center", va="center", fontsize=14)

fpr, tpr, _ = roc_curve(y_test, rf_probs)
axes[1].plot(fpr, tpr, color="#2C7FB8", label=f"AUC = {roc_auc_score(y_test, rf_probs):.3f}")
axes[1].plot([0, 1], [0, 1], linestyle="--", color="gray")
axes[1].set_title("ROC Curve")
axes[1].set_xlabel("False Positive Rate")
axes[1].set_ylabel("True Positive Rate")
axes[1].legend()
plt.tight_layout()
plt.savefig("charts/03_evaluation.png", dpi=150)
plt.close()


# =============================================================================
# CLIP 12 — Feature importance chart
# =============================================================================
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8, 5))
importances.sort_values().plot(kind="barh", ax=ax, color="#2C7FB8")
ax.set_title("Top 10 Feature Importances — Random Forest")
ax.set_xlabel("Importance")
plt.tight_layout()
plt.savefig("charts/04_feature_importance.png", dpi=150)
plt.close()

print("\nTop features driving default risk:")
print(importances.sort_values(ascending=False))


# =============================================================================
# CLIP 13 — Key takeaway
# =============================================================================
print("\n--- Summary ---")
print(f"Baseline (Logistic Regression) ROC-AUC: {roc_auc_score(y_test, logreg_probs):.3f}")
print(f"Random Forest ROC-AUC: {roc_auc_score(y_test, rf_probs):.3f}")
print("Charts saved to ./charts/")
