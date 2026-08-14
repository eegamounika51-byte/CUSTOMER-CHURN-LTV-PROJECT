import pandas as pd
import matplotlib.pyplot as plt
import shap
import joblib
import os

from sklearn.model_selection import train_test_split


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

print("Dataset loaded successfully!")


# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = df.columns.str.strip()


# ==========================================
# CONVERT CHURN TO 0/1
# ==========================================

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ==========================================
# REMOVE CUSTOMER ID
# ==========================================

if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = df.drop(columns=["Churn"])
y = df["Churn"]


# ==========================================
# ENCODE CATEGORICAL VARIABLES
# ==========================================

X = pd.get_dummies(
    X,
    drop_first=True
)


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

X = X.fillna(0)


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# LOAD XGBOOST MODEL
# ==========================================

model = joblib.load(
    "models/xgboost_churn_model.pkl"
)


print("XGBoost model loaded successfully!")


# ==========================================
# CREATE SHAP EXPLAINER
# ==========================================

explainer = shap.TreeExplainer(model)


# Calculate SHAP values
shap_values = explainer.shap_values(X_test)


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

os.makedirs("outputs", exist_ok=True)


# ==========================================
# SHAP SUMMARY PLOT
# ==========================================

plt.figure()

shap.summary_plot(
    shap_values,
    X_test,
    show=False
)

plt.title(
    "SHAP Feature Importance - Customer Churn"
)

plt.tight_layout()

plt.savefig(
    "outputs/shap_summary.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================
# SHAP BAR PLOT
# ==========================================

plt.figure()

shap.summary_plot(
    shap_values,
    X_test,
    plot_type="bar",
    show=False
)

plt.title(
    "SHAP Global Feature Importance"
)

plt.tight_layout()

plt.savefig(
    "outputs/shap_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================
# SAVE SHAP VALUES
# ==========================================

shap_df = pd.DataFrame(
    shap_values,
    columns=X_test.columns,
    index=X_test.index
)

shap_df.to_csv(
    "outputs/shap_values.csv"
)


# ==========================================
# DISPLAY TOP FEATURES
# ==========================================

mean_abs_shap = (
    shap_df.abs()
    .mean()
    .sort_values(ascending=False)
)

print("\n==========================================")
print("TOP SHAP FEATURES")
print("==========================================")

print(
    mean_abs_shap.head(15)
)


print("\n==========================================")
print("SHAP EXPLAINABILITY COMPLETED")
print("==========================================")

print("\nGenerated files:")
print("outputs/shap_summary.png")
print("outputs/shap_feature_importance.png")
print("outputs/shap_values.csv")

print("\nSTEP 39 COMPLETED SUCCESSFULLY!")