import pandas as pd
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

print("Dataset loaded successfully!")
print("Shape:", df.shape)

# Create target
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Separate features and target
X = df.drop(columns=["Churn"])
y = df["Churn"]

# Convert categorical columns
X = pd.get_dummies(X, drop_first=True)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n===== TRAIN TEST SPLIT =====")
print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

print("\nTrain-Test Split completed successfully!")