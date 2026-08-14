import pandas as pd
import os


# ==========================================
# LOAD RETENTION DATA
# ==========================================

input_file = "outputs/retention_priority_scores.csv"

df = pd.read_csv(input_file)

print("Retention data loaded!")
print("Total customers:", len(df))


# ==========================================
# CREATE DASHBOARD FOLDER
# ==========================================

os.makedirs("dashboard/data", exist_ok=True)


# ==========================================
# 1. CUSTOMER RISK DATA
# ==========================================

risk_data = df[
    [
        "customer_id",
        "churn_probability",
        "churn_risk",
        "ltv",
        "customer_segment",
        "retention_priority_score",
        "retention_priority"
    ]
].copy()

risk_data.to_csv(
    "dashboard/data/churn_risk_data.csv",
    index=False
)


# ==========================================
# 2. LTV SEGMENT DATA
# ==========================================

ltv_data = df[
    [
        "customer_id",
        "ltv",
        "ltv_segment",
        "churn_risk",
        "customer_segment"
    ]
].copy()

ltv_data.to_csv(
    "dashboard/data/ltv_segment_data.csv",
    index=False
)


# ==========================================
# 3. RETENTION DATA
# ==========================================

retention_data = df[
    [
        "customer_id",
        "ltv",
        "churn_probability",
        "customer_segment",
        "retention_priority_score",
        "retention_priority",
        "recommended_action"
    ]
].copy()

retention_data.to_csv(
    "dashboard/data/retention_data.csv",
    index=False
)


# ==========================================
# 4. SUMMARY DATA
# ==========================================

summary = pd.DataFrame({
    "Metric": [
        "Total Customers",
        "High Risk Customers",
        "Critical Customers",
        "High Priority Customers",
        "Average LTV",
        "Average Churn Probability"
    ],

    "Value": [
        len(df),

        len(
            df[
                df["churn_risk"] == "High Risk"
            ]
        ),

        len(
            df[
                df["retention_priority"] == "Critical"
            ]
        ),

        len(
            df[
                df["retention_priority"] == "High"
            ]
        ),

        round(
            df["ltv"].mean(),
            2
        ),

        round(
            df["churn_probability"].mean(),
            4
        )
    ]
})


summary.to_csv(
    "dashboard/data/dashboard_summary.csv",
    index=False
)


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("DASHBOARD DATA PREPARATION")
print("==========================================")

print("\nSummary:")
print(summary)

print("\nCreated files:")

print("dashboard/data/churn_risk_data.csv")
print("dashboard/data/ltv_segment_data.csv")
print("dashboard/data/retention_data.csv")
print("dashboard/data/dashboard_summary.csv")


# ==========================================
# COMPLETED
# ==========================================

print("\n==========================================")
print("STEP 50 COMPLETED SUCCESSFULLY!")
print("==========================================")