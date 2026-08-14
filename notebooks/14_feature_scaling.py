import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean numeric columns
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Create target variable
df["Churn_Encoded"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Remove unnecessary columns if they exist
columns_to_drop = ["Churn", "customerID"]

for column in columns_to_drop:
    if column in df.columns:
        df = df.drop(columns=[column])

# Convert categorical columns
categorical_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

df = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True
)

# Separate features and target
X = df.drop(columns=["Churn_Encoded"])
y = df["Churn_Encoded"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Select numerical columns
numeric_columns = X_train.select_dtypes(
    include=["int64", "float64"]
).columns

# Create scaler
scaler = StandardScaler()

# Fit scaler ONLY on training data
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[numeric_columns] = scaler.fit_transform(
    X_train[numeric_columns]
)

X_test_scaled[numeric_columns] = scaler.transform(
    X_test[numeric_columns]
)

print("========== FEATURE SCALING ==========")

print("Original training shape:", X_train.shape)
print("Scaled training shape:", X_train_scaled.shape)

print("\nOriginal numeric values:")
print(X_train[numeric_columns].head())

print("\nScaled numeric values:")
print(X_train_scaled[numeric_columns].head())

print("\nFeature scaling completed successfully!")