import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from xgboost import XGBClassifier


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
# SEPARATE FEATURES AND TARGET
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
# XGBOOST MODEL
# ==========================================

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)


# ==========================================
# TRAIN MODEL
# ==========================================

xgb_model.fit(
    X_train,
    y_train
)


# ==========================================
# PREDICTIONS
# ==========================================

xgb_pred = xgb_model.predict(X_test)

xgb_prob = xgb_model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# MODEL METRICS
# ==========================================

xgb_accuracy = accuracy_score(
    y_test,
    xgb_pred
)

xgb_f1 = f1_score(
    y_test,
    xgb_pred
)

xgb_auc = roc_auc_score(
    y_test,
    xgb_prob
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("XGBOOST MODEL PERFORMANCE")
print("==========================================")

print(
    "Accuracy:",
    round(xgb_accuracy * 100, 2),
    "%"
)

print(
    "F1 Score:",
    round(xgb_f1 * 100, 2),
    "%"
)

print(
    "ROC-AUC:",
    round(xgb_auc, 4)
)


# ==========================================
# SAVE MODEL
# ==========================================

import os
import joblib

os.makedirs("models", exist_ok=True)

joblib.dump(
    xgb_model,
    "models/xgboost_churn_model.pkl"
)


print("\nModel saved successfully:")
print("models/xgboost_churn_model.pkl")

print("\nSTEP 38 COMPLETED SUCCESSFULLY!")