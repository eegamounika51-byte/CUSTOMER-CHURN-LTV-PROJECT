import pandas as pd

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Convert MonthlyCharges to numeric
df["MonthlyCharges"] = pd.to_numeric(
    df["MonthlyCharges"],
    errors="coerce"
)

# Average monthly charges by churn status
monthly_charges = df.groupby("Churn")["MonthlyCharges"].agg(
    ["count", "mean", "median", "min", "max"]
)

print("========== MONTHLY CHARGES BY CHURN ==========")
print(monthly_charges.round(2))

# Create monthly charge groups
def charge_group(amount):
    if amount < 30:
        return "Low (<30)"
    elif amount < 60:
        return "Medium (30-60)"
    elif amount < 90:
        return "High (60-90)"
    else:
        return "Very High (90+)"

df["MonthlyChargeGroup"] = df["MonthlyCharges"].apply(charge_group)

# Churn percentage by charge group
charge_churn = pd.crosstab(
    df["MonthlyChargeGroup"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== CHURN BY MONTHLY CHARGE GROUP ==========")
print(charge_churn.round(2))