import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")


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
# SEPARATE X AND Y
# ==========================================

X = df.drop(columns=["Churn"])
y = df["Churn"]


# ==========================================
# ENCODE CATEGORICAL COLUMNS
# ==========================================

X = pd.get_dummies(X, drop_first=True)


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
# RANDOM FOREST MODEL
# ==========================================

random_forest_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

random_forest_model.fit(
    X_train,
    y_train
)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

feature_importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": random_forest_model.feature_importances_
})


# Sort by importance
feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("========== FEATURE IMPORTANCE ==========")

print(feature_importance.to_string(index=False))


# ==========================================
# TOP 15 FEATURES
# ==========================================

top_features = feature_importance.head(15)


print("\n========== TOP 15 IMPORTANT FEATURES ==========")

print(top_features.to_string(index=False))


# ==========================================
# BAR CHART
# ==========================================

plt.figure(figsize=(10, 7))

plt.barh(
    top_features["Feature"][::-1],
    top_features["Importance"][::-1]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 15 Features Influencing Customer Churn")

plt.tight_layout()

plt.savefig("feature_importance.png", dpi=300)

plt.show()


print("\nSTEP 32 COMPLETED SUCCESSFULLY!")