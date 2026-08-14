import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# ==========================================
# 2. CREATE TARGET VARIABLE
# ==========================================

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ==========================================
# 3. REMOVE UNNECESSARY COLUMNS
# ==========================================

if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])


# ==========================================
# 4. SEPARATE FEATURES AND TARGET
# ==========================================

X = df.drop(columns=["Churn"])
y = df["Churn"]


# ==========================================
# 5. ENCODE CATEGORICAL COLUMNS
# ==========================================

X = pd.get_dummies(
    X,
    drop_first=True
)


# ==========================================
# 6. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# 7. FEATURE SCALING
# ==========================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ==========================================
# 8. CREATE LOGISTIC REGRESSION MODEL
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


# ==========================================
# 9. TRAIN MODEL
# ==========================================

model.fit(
    X_train_scaled,
    y_train
)

print("\nModel training completed successfully!")


# ==========================================
# 10. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test_scaled)


# ==========================================
# 11. MODEL ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n========== MODEL ACCURACY ==========")
print("Accuracy:", round(accuracy * 100, 2), "%")


# ==========================================
# 12. CLASSIFICATION REPORT
# ==========================================

print("\n========== CLASSIFICATION REPORT ==========")

print(
    classification_report(
        y_test,
        y_pred
    )
)

print("\nSTEP 26 COMPLETED SUCCESSFULLY!")