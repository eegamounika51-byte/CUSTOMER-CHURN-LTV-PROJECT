import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Convert Churn to 0/1
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Remove customerID if available
if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])

# Separate X and y
X = df.drop(columns=["Churn"])
y = df["Churn"]

# Encode categorical columns
X = pd.get_dummies(X, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Scale data for Logistic Regression
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================
# LOGISTIC REGRESSION
# ==========================================

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
# MODEL COMPARISON
# ==========================================

logistic_accuracy = accuracy_score(
    y_test,
    logistic_pred
)

logistic_f1 = f1_score(
    y_test,
    logistic_pred
)

logistic_auc = roc_auc_score(
    y_test,
    logistic_prob
)


rf_accuracy = accuracy_score(
    y_test,
    rf_pred
)

rf_f1 = f1_score(
    y_test,
    rf_pred
)

rf_auc = roc_auc_score(
    y_test,
    rf_prob
)


print("========== MODEL COMPARISON ==========")

print("\nLogistic Regression")
print("-------------------")
print("Accuracy:", round(logistic_accuracy * 100, 2), "%")
print("F1 Score:", round(logistic_f1 * 100, 2), "%")
print("AUC     :", round(logistic_auc, 4))


print("\nRandom Forest")
print("-------------------")
print("Accuracy:", round(rf_accuracy * 100, 2), "%")
print("F1 Score:", round(rf_f1 * 100, 2), "%")
print("AUC     :", round(rf_auc, 4))


print("\nSTEP 31 COMPLETED SUCCESSFULLY!")