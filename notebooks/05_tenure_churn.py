import pandas as pd

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Create tenure groups
def tenure_group(months):
    if months <= 12:
        return "0-12 Months"
    elif months <= 24:
        return "13-24 Months"
    elif months <= 48:
        return "25-48 Months"
    else:
        return "49+ Months"

df["TenureGroup"] = df["tenure"].apply(tenure_group)

# Count customers in each tenure group
print("========== CUSTOMERS BY TENURE GROUP ==========")
print(df["TenureGroup"].value_counts().sort_index())

# Churn count
tenure_churn = pd.crosstab(
    df["TenureGroup"],
    df["Churn"]
)

print("\n========== TENURE-WISE CHURN ==========")
print(tenure_churn)

# Churn percentage
tenure_churn_percentage = pd.crosstab(
    df["TenureGroup"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== TENURE-WISE CHURN PERCENTAGE ==========")
print(tenure_churn_percentage.round(2))