import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


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

# Scale features
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

# Predictions
y_pred = model.predict(X_test_scaled)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

print("========== CONFUSION MATRIX ==========")
print(cm)

# Display matrix
plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Stayed", "Churned"],
    yticklabels=["Stayed", "Churned"]
)

plt.title("Customer Churn - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()
plt.show()

print("\nSTEP 27 COMPLETED SUCCESSFULLY!")