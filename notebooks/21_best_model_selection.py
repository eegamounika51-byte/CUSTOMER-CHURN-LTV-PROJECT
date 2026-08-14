import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


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


# Remove customer ID
if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])


# ==========================================
# FEATURES AND TARGET
# ==========================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

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
# LOGISTIC REGRESSION
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic_model.fit(
    X_train_scaled,
    y_train
)

logistic_pred = logistic_model.predict(X_test_scaled)
logistic_prob = logistic_model.predict_proba(X_test_scaled)[:, 1]


# ==========================================
# RANDOM FOREST
# ==========================================

random_forest_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

random_forest_model.fit(
    X_train,
    y_train
)

rf_pred = random_forest_model.predict(X_test)
rf_prob = random_forest_model.predict_proba(X_test)[:, 1]


# ==========================================
# CALCULATE METRICS
# ==========================================

logistic_accuracy = accuracy_score(y_test, logistic_pred)
logistic_f1 = f1_score(y_test, logistic_pred)
logistic_auc = roc_auc_score(y_test, logistic_prob)

rf_accuracy = accuracy_score(y_test, rf_pred)
rf_f1 = f1_score(y_test, rf_pred)
rf_auc = roc_auc_score(y_test, rf_prob)


# ==========================================
# MODEL COMPARISON TABLE
# ==========================================

results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Random Forest"
    ],
    "Accuracy": [
        logistic_accuracy,
        rf_accuracy
    ],
    "F1 Score": [
        logistic_f1,
        rf_f1
    ],
    "AUC": [
        logistic_auc,
        rf_auc
    ]
})


print("========== MODEL PERFORMANCE ==========\n")

print(results.to_string(index=False))


# ==========================================
# BEST MODEL SELECTION
# ==========================================

# F1 Score is used as the main selection metric
best_model_name = results.loc[
    results["F1 Score"].idxmax(),
    "Model"
]

best_f1 = results["F1 Score"].max()


print("\n========================================")
print("BEST MODEL SELECTION")
print("========================================")

print("Best Model :", best_model_name)
print("Best F1 Score :", round(best_f1, 4))


# ==========================================
# FINAL DECISION
# ==========================================

if best_model_name == "Random Forest":

    best_model = random_forest_model

else:

    best_model = logistic_model


print("\nSelected Model:", best_model_name)

print("\nSTEP 33 COMPLETED SUCCESSFULLY!")