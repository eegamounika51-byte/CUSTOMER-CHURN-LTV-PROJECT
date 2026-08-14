import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score


# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Convert Churn to numbers
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Remove customerID if available
if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])

# Separate features and target
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

# Feature scaling
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create model
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

# Train model
model.fit(X_train_scaled, y_train)

# Get churn probabilities
y_probability = model.predict_proba(X_test_scaled)[:, 1]

# Calculate ROC values
fpr, tpr, thresholds = roc_curve(
    y_test,
    y_probability
)

# Calculate AUC
auc_score = roc_auc_score(
    y_test,
    y_probability
)

print("========== ROC-AUC RESULT ==========")
print("AUC Score:", round(auc_score, 4))

# Plot ROC Curve
plt.figure(figsize=(8, 6))

plt.plot(
    fpr,
    tpr,
    label=f"Logistic Regression (AUC = {auc_score:.2f})"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Model"
)

plt.title("ROC Curve - Customer Churn Prediction")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.legend()
plt.tight_layout()
plt.show()

print("\nSTEP 29 COMPLETED SUCCESSFULLY!")