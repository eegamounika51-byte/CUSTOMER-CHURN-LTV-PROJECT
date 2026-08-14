import pandas as pd

# Load dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Internet service customer count
internet_count = df["InternetService"].value_counts()

print("========== CUSTOMERS BY INTERNET SERVICE ==========")
print(internet_count)

# Internet service-wise churn count
internet_churn = pd.crosstab(
    df["InternetService"],
    df["Churn"]
)

print("\n========== INTERNET SERVICE-WISE CHURN ==========")
print(internet_churn)

# Internet service-wise churn percentage
internet_churn_percentage = pd.crosstab(
    df["InternetService"],
    df["Churn"],
    normalize="index"
) * 100

print("\n========== INTERNET SERVICE-WISE CHURN PERCENTAGE ==========")
print(internet_churn_percentage.round(2))