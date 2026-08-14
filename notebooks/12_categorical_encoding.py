import pandas as pd

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Encode target
df["Churn_Encoded"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# Remove customer ID because it is not useful for prediction

# Convert categorical columns into dummy variables
categorical_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

# Don't encode original Churn column
categorical_columns.remove("Churn")

df_encoded = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True
)

print("========== ORIGINAL SHAPE ==========")
print(df.shape)

print("\n========== ENCODED SHAPE ==========")
print(df_encoded.shape)

print("\n========== ENCODED COLUMNS ==========")
print(df_encoded.columns.tolist())

print("\n========== FIRST 5 ROWS ==========")
print(df_encoded.head())

print("\nCategorical encoding completed successfully!")