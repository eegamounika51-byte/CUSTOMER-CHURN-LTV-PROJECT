import pandas as pd

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Contract-wise customer count
contract_count = df["Contract"].value_counts()

print("========== CUSTOMERS BY CONTRACT ==========")
print(contract_count)

# Contract-wise churn count
contract_churn = pd.crosstab(df["Contract"], df["Churn"])

print("\n========== CONTRACT-WISE CHURN ==========")
print(contract_churn)

# Contract-wise churn percentage
contract_churn_percentage = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== CONTRACT-WISE CHURN PERCENTAGE ==========")
print(contract_churn_percentage.round(2))