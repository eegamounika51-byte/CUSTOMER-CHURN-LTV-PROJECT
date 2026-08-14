import pandas as pd

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean numeric columns
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df["TotalCharges"] = df["TotalCharges"].fillna(0)

df["MonthlyCharges"] = pd.to_numeric(
    df["MonthlyCharges"],
    errors="coerce"
)

# -----------------------------
# BASIC SUMMARY
# -----------------------------

total_customers = len(df)

churned = (df["Churn"] == "Yes").sum()
stayed = (df["Churn"] == "No").sum()

churn_rate = (churned / total_customers) * 100

print("========== EDA SUMMARY ==========")

print("Total Customers:", total_customers)
print("Churned Customers:", churned)
print("Customers Stayed:", stayed)
print("Overall Churn Rate:", round(churn_rate, 2), "%")


# -----------------------------
# CONTRACT INSIGHT
# -----------------------------

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== CONTRACT CHURN RATE ==========")
print(contract_churn.round(2))


# -----------------------------
# INTERNET SERVICE INSIGHT
# -----------------------------

internet_churn = pd.crosstab(
    df["InternetService"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== INTERNET SERVICE CHURN RATE ==========")
print(internet_churn.round(2))


# -----------------------------
# TENURE INSIGHT
# -----------------------------

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

tenure_churn = pd.crosstab(
    df["TenureGroup"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== TENURE CHURN RATE ==========")
print(tenure_churn.round(2))


# -----------------------------
# MONTHLY CHARGES INSIGHT
# -----------------------------

monthly_charges = df.groupby("Churn")["MonthlyCharges"].mean()

print("\n========== AVERAGE MONTHLY CHARGES ==========")
print(monthly_charges.round(2))


print("\n========== EDA COMPLETED ==========")
print("The dataset is ready for feature engineering and machine learning.")