import pandas as pd

# Load Excel dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

print("Original shape:", df.shape)

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Check missing values again
print("\nMissing TotalCharges after conversion:")
print(df["TotalCharges"].isnull().sum())

# Fill missing TotalCharges with 0
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Remove duplicate rows
df = df.drop_duplicates()

print("\nFinal shape:", df.shape)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nCleaning completed successfully!")