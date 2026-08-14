import pandas as pd

# Load cleaned dataset
df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

# Clean TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Churn count
churn_count = df["Churn"].value_counts()

print("========== CHURN COUNT ==========")
print(churn_count)

# Churn percentage
churn_percentage = df["Churn"].value_counts(normalize=True) * 100

print("\n========== CHURN PERCENTAGE ==========")
print(churn_percentage.round(2))

# Simple summary
total_customers = len(df)
churned_customers = (df["Churn"] == "Yes").sum()
stayed_customers = (df["Churn"] == "No").sum()

print("\n========== SUMMARY ==========")
print("Total Customers:", total_customers)
print("Churned Customers:", churned_customers)
print("Customers Stayed:", stayed_customers)
print("Churn Rate:", round((churned_customers / total_customers) * 100, 2), "%")