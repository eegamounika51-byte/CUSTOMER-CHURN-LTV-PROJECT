import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# CREATE OUTPUT FOLDERS
# ==========================================

os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")


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
# TRAIN FINAL RANDOM FOREST MODEL
# ==========================================

final_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

final_model.fit(
    X_train,
    y_train
)


# ==========================================
# SAVE FINAL MODEL
# ==========================================

joblib.dump(
    final_model,
    "models/final_churn_model.pkl"
)


# ==========================================
# SAVE FEATURE NAMES
# ==========================================

feature_names = pd.DataFrame({
    "Feature": X_train.columns
})

feature_names.to_csv(
    "outputs/final_feature_names.csv",
    index=False
)


# ==========================================
# SAVE FEATURE IMPORTANCE
# ==========================================

feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": final_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

feature_importance.to_csv(
    "outputs/final_feature_importance.csv",
    index=False
)


# ==========================================
# SAVE TEST DATA
# ==========================================

test_data = X_test.copy()

test_data["Actual_Churn"] = y_test.values

test_data.to_csv(
    "outputs/test_predictions_input.csv",
    index=False
)


# ==========================================
# FINAL MESSAGE
# ==========================================

print("==========================================")
print("FINAL MODEL SAVING COMPLETED")
print("==========================================")

print("\nFinal Model:")
print("models/final_churn_model.pkl")

print("\nSaved Outputs:")
print("outputs/final_feature_names.csv")
print("outputs/final_feature_importance.csv")
print("outputs/test_predictions_input.csv")

print("\nSTEP 36 COMPLETED SUCCESSFULLY!")