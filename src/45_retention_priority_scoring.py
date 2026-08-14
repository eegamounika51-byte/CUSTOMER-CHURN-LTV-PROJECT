import pandas as pd


# =========================================================
# STEP 45
# RETENTION PRIORITY SCORING
# =========================================================


# =========================================================
# 1. LOAD STEP 44 OUTPUT
# =========================================================

input_file = "outputs/churn_ltv_segments.csv"

df = pd.read_csv(input_file)

print("Churn + LTV segmentation loaded!")
print("Total customers:", len(df))


# =========================================================
# 2. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "customer_id",
    "ltv",
    "churn_probability",
    "churn_risk",
    "ltv_segment",
    "customer_segment"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# =========================================================
# 3. CLEAN VALUES
# =========================================================

df["ltv"] = pd.to_numeric(
    df["ltv"],
    errors="coerce"
).fillna(0)

df["churn_probability"] = pd.to_numeric(
    df["churn_probability"],
    errors="coerce"
).fillna(0)


# Make sure probability is between 0 and 1

df["churn_probability"] = (
    df["churn_probability"]
    .clip(0, 1)
)


# =========================================================
# 4. NORMALIZE LTV
# =========================================================

max_ltv = df["ltv"].max()

if max_ltv > 0:

    df["ltv_score"] = (
        df["ltv"] / max_ltv
    ) * 100

else:

    df["ltv_score"] = 0


# =========================================================
# 5. CHURN RISK SCORE
# =========================================================

df["churn_score"] = (
    df["churn_probability"] * 100
)


# =========================================================
# 6. RETENTION PRIORITY SCORE
# =========================================================
#
# Higher churn probability = higher priority
# Higher LTV = higher priority
#
# 60% weight = churn risk
# 40% weight = customer value
# =========================================================

df["retention_priority_score"] = (
    (df["churn_score"] * 0.60)
    +
    (df["ltv_score"] * 0.40)
)


# =========================================================
# 7. ROUND SCORE
# =========================================================

df["retention_priority_score"] = (
    df["retention_priority_score"]
    .round(2)
)


# =========================================================
# 8. PRIORITY CATEGORY
# =========================================================

def get_priority(score):

    if score >= 75:

        return "Critical"

    elif score >= 50:

        return "High"

    elif score >= 25:

        return "Medium"

    else:

        return "Low"


df["retention_priority"] = (
    df["retention_priority_score"]
    .apply(get_priority)
)


# =========================================================
# 9. RECOMMENDED ACTION
# =========================================================

def get_action(row):

    priority = row["retention_priority"]
    segment = row["customer_segment"]


    if priority == "Critical":

        return "Immediate retention intervention"


    elif priority == "High":

        return "Offer discount / loyalty benefit"


    elif priority == "Medium":

        return "Monitor and engage"


    else:

        return "Standard customer engagement"


df["recommended_action"] = df.apply(
    get_action,
    axis=1
)


# =========================================================
# 10. SORT BY PRIORITY
# =========================================================

df = df.sort_values(
    by="retention_priority_score",
    ascending=False
)


# =========================================================
# 11. DISPLAY TOP PRIORITY CUSTOMERS
# =========================================================

print("\n================================================")
print("TOP RETENTION PRIORITY CUSTOMERS")
print("================================================")


display_columns = [
    "customer_id",
    "ltv",
    "churn_probability",
    "churn_risk",
    "ltv_segment",
    "customer_segment",
    "retention_priority_score",
    "retention_priority",
    "recommended_action"
]


print(
    df[
        display_columns
    ].head(20)
)


# =========================================================
# 12. PRIORITY DISTRIBUTION
# =========================================================

print("\n================================================")
print("RETENTION PRIORITY DISTRIBUTION")
print("================================================")

print(
    df["retention_priority"]
    .value_counts()
)


# =========================================================
# 13. SAVE COMPLETE DATA
# =========================================================

output_file = (
    "outputs/retention_priority_scores.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\nRetention priority data saved to:")

print(output_file)


# =========================================================
# 14. SAVE CRITICAL CUSTOMERS
# =========================================================

critical_customers = df[
    df["retention_priority"] == "Critical"
].copy()


critical_file = (
    "outputs/critical_retention_customers.csv"
)

critical_customers.to_csv(
    critical_file,
    index=False
)


print("\nCritical customers saved to:")

print(critical_file)


# =========================================================
# 15. SUMMARY
# =========================================================

print("\n================================================")
print("RETENTION SUMMARY")
print("================================================")

print(
    "Total Customers:",
    len(df)
)

print(
    "Critical:",
    len(
        df[
            df["retention_priority"] == "Critical"
        ]
    )
)

print(
    "High:",
    len(
        df[
            df["retention_priority"] == "High"
        ]
    )
)

print(
    "Medium:",
    len(
        df[
            df["retention_priority"] == "Medium"
        ]
    )
)

print(
    "Low:",
    len(
        df[
            df["retention_priority"] == "Low"
        ]
    )
)


# =========================================================
# 16. COMPLETED
# =========================================================

print("\n================================================")
print("STEP 45 COMPLETED SUCCESSFULLY!")
print("================================================")
