import pandas as pd


# =========================================================
# STEP 44
# CHURN + LTV CUSTOMER SEGMENTATION
# =========================================================


# =========================================================
# 1. LOAD LTV DATA
# =========================================================

ltv_file = "outputs/ltv_features.csv"

df_ltv = pd.read_csv(ltv_file)

print("LTV data loaded successfully!")
print("LTV rows:", len(df_ltv))

print("\nLTV columns:")
print(df_ltv.columns.tolist())


# =========================================================
# 2. LOAD FINAL CHURN PREDICTIONS
# =========================================================

prediction_file = "final_churn_predictions.csv"

df_pred = pd.read_csv(prediction_file)

print("\nChurn prediction data loaded successfully!")
print("Prediction rows:", len(df_pred))

print("\nPrediction columns:")
print(df_pred.columns.tolist())


# =========================================================
# 3. CLEAN COLUMN NAMES
# =========================================================

df_ltv.columns = (
    df_ltv.columns
    .str.strip()
)

df_pred.columns = (
    df_pred.columns
    .str.strip()
)


# =========================================================
# 4. CUSTOMER ID FROM LTV DATA
# =========================================================

customer_columns = [
    "customer_id",
    "customerID",
    "customer",
    "CustomerID",
    "Customer_ID"
]

ltv_customer_column = None

for column in customer_columns:

    if column in df_ltv.columns:

        ltv_customer_column = column
        break


if ltv_customer_column is None:

    raise ValueError(
        "Customer ID column not found in ltv_features.csv"
    )


# Rename customer ID
df_ltv = df_ltv.rename(
    columns={
        ltv_customer_column: "customer_id"
    }
)


# =========================================================
# 5. FIND CUSTOMER ID IN PREDICTION FILE
# =========================================================

pred_customer_column = None

for column in customer_columns:

    if column in df_pred.columns:

        pred_customer_column = column
        break


# ---------------------------------------------------------
# IMPORTANT:
# If prediction file does NOT contain customer ID,
# match predictions by row order.
# ---------------------------------------------------------

if pred_customer_column is not None:

    df_pred = df_pred.rename(
        columns={
            pred_customer_column: "customer_id"
        }
    )

    df_ltv["customer_id"] = (
        df_ltv["customer_id"]
        .astype(str)
    )

    df_pred["customer_id"] = (
        df_pred["customer_id"]
        .astype(str)
    )

    merge_by_customer = True

else:

    print(
        "\nCustomer ID not found in prediction file."
    )

    print(
        "Predictions will be matched using row order."
    )

    merge_by_customer = False


# =========================================================
# 6. FIND PREDICTED CHURN COLUMN
# =========================================================

prediction_columns = [
    "Predicted_Churn",
    "predicted_churn",
    "Prediction",
    "prediction",
    "Churn_Prediction",
    "churn_prediction",
    "PredictedChurn"
]

churn_column = None

for column in prediction_columns:

    if column in df_pred.columns:

        churn_column = column
        break


if churn_column is None:

    raise ValueError(
        "Predicted churn column not found."
    )


# =========================================================
# 7. FIND CHURN PROBABILITY COLUMN
# =========================================================

probability_columns = [
    "Churn_Probability",
    "churn_probability",
    "Probability",
    "probability",
    "Churn Probability",
    "ChurnProbability"
]

probability_column = None

for column in probability_columns:

    if column in df_pred.columns:

        probability_column = column
        break


if probability_column is None:

    raise ValueError(
        "Churn probability column not found."
    )


print("\nDetected churn column:")
print(churn_column)

print("\nDetected probability column:")
print(probability_column)


# =========================================================
# 8. PREPARE PREDICTION DATA
# =========================================================

df_pred = df_pred.rename(
    columns={
        churn_column: "predicted_churn",
        probability_column: "churn_probability"
    }
)


# =========================================================
# 9. MERGE LTV + CHURN
# =========================================================

if merge_by_customer:

    df = df_ltv.merge(
        df_pred[
            [
                "customer_id",
                "predicted_churn",
                "churn_probability"
            ]
        ],
        on="customer_id",
        how="left"
    )

else:

    # Match using row order

    if len(df_ltv) != len(df_pred):

        raise ValueError(
            "LTV rows and prediction rows are different. "
            "Cannot safely match predictions by row order."
        )

    df = df_ltv.copy()

    df["predicted_churn"] = (
        df_pred["predicted_churn"].values
    )

    df["churn_probability"] = (
        df_pred["churn_probability"].values
    )


print("\nLTV + Churn data merged successfully!")

print("Final rows:", len(df))


# =========================================================
# 10. CLEAN CHURN PROBABILITY
# =========================================================

df["churn_probability"] = pd.to_numeric(
    df["churn_probability"],
    errors="coerce"
)

df["churn_probability"] = (
    df["churn_probability"]
    .fillna(0)
)


# =========================================================
# 11. HANDLE PROBABILITY FORMAT
# =========================================================

# If probability is stored as percentage,
# convert it to 0-1.

if df["churn_probability"].max() > 1:

    df["churn_probability"] = (
        df["churn_probability"] / 100
    )


# =========================================================
# 12. CHURN RISK CATEGORY
# =========================================================

def get_churn_risk(probability):

    if probability >= 0.70:

        return "High Risk"

    elif probability >= 0.40:

        return "Medium Risk"

    else:

        return "Low Risk"


df["churn_risk"] = (
    df["churn_probability"]
    .apply(get_churn_risk)
)


# =========================================================
# 13. CLEAN LTV
# =========================================================

df["ltv"] = pd.to_numeric(
    df["ltv"],
    errors="coerce"
)

df["ltv"] = df["ltv"].fillna(0)


# =========================================================
# 14. LTV SEGMENT
# =========================================================

def get_ltv_segment(value):

    if value >= 6000:

        return "Very High Value"

    elif value >= 3000:

        return "High Value"

    elif value >= 1000:

        return "Medium Value"

    else:

        return "Low Value"


df["ltv_segment"] = (
    df["ltv"]
    .apply(get_ltv_segment)
)


# =========================================================
# 15. CUSTOMER SEGMENT
# =========================================================

def get_customer_segment(row):

    risk = row["churn_risk"]
    value = row["ltv_segment"]


    # Highest priority
    if (
        risk == "High Risk"
        and value == "Very High Value"
    ):

        return "Critical - High Value"


    # High value and high churn risk
    elif (
        risk == "High Risk"
        and value == "High Value"
    ):

        return "High Value At Risk"


    # Other high risk
    elif risk == "High Risk":

        return "Churn Risk"


    # VIP customers
    elif value == "Very High Value":

        return "VIP Customer"


    # High value customers
    elif value == "High Value":

        return "High Value Customer"


    # Medium risk
    elif risk == "Medium Risk":

        return "Monitor"


    # Remaining customers
    else:

        return "Low Priority"


df["customer_segment"] = df.apply(
    get_customer_segment,
    axis=1
)


# =========================================================
# 16. DISPLAY SEGMENT DISTRIBUTION
# =========================================================

print("\n================================================")
print("CUSTOMER SEGMENT DISTRIBUTION")
print("================================================")

print(
    df["customer_segment"]
    .value_counts()
)


# =========================================================
# 17. DISPLAY CHURN RISK DISTRIBUTION
# =========================================================

print("\n================================================")
print("CHURN RISK DISTRIBUTION")
print("================================================")

print(
    df["churn_risk"]
    .value_counts()
)


# =========================================================
# 18. DISPLAY LTV DISTRIBUTION
# =========================================================

print("\n================================================")
print("LTV SEGMENT DISTRIBUTION")
print("================================================")

print(
    df["ltv_segment"]
    .value_counts()
)


# =========================================================
# 19. HIGH VALUE AT RISK CUSTOMERS
# =========================================================

high_value_risk = df[
    df["customer_segment"].isin(
        [
            "Critical - High Value",
            "High Value At Risk"
        ]
    )
].copy()


high_value_risk = high_value_risk.sort_values(
    by="churn_probability",
    ascending=False
)


print("\n================================================")
print("HIGH-VALUE CUSTOMERS AT RISK")
print("================================================")


display_columns = [
    "customer_id",
    "ltv",
    "churn_probability",
    "predicted_churn",
    "churn_risk",
    "ltv_segment",
    "customer_segment"
]


print(
    high_value_risk[
        display_columns
    ].head(20)
)


# =========================================================
# 20. SAVE COMPLETE SEGMENTATION
# =========================================================

output_file = (
    "outputs/churn_ltv_segments.csv"
)

df.to_csv(
    output_file,
    index=False
)


print("\nComplete segmentation saved to:")

print(output_file)


# =========================================================
# 21. SAVE HIGH-VALUE AT-RISK CUSTOMERS
# =========================================================

risk_file = (
    "outputs/high_value_at_risk_customers.csv"
)

high_value_risk.to_csv(
    risk_file,
    index=False
)


print("\nHigh-value at-risk customers saved to:")

print(risk_file)


# =========================================================
# 22. SUMMARY
# =========================================================

print("\n================================================")
print("STEP 44 SUMMARY")
print("================================================")

print(
    "Total Customers:",
    len(df)
)

print(
    "High Risk Customers:",
    len(
        df[
            df["churn_risk"] == "High Risk"
        ]
    )
)

print(
    "High-Value At-Risk Customers:",
    len(high_value_risk)
)

print(
    "Average LTV:",
    round(df["ltv"].mean(), 2)
)


# =========================================================
# 23. COMPLETED
#