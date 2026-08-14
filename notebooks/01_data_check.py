import pandas as pd

df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

print("========== DATASET INFO ==========")
print(df.info())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

print("\n========== CHURN VALUES ==========")
print(df["Churn"].value_counts())

print("\n========== STATISTICS ==========")
print(df.describe())