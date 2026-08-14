import pandas as pd


# ==========================================
# LOAD FINAL PREDICTIONS
# ==========================================

df = pd.read_csv("final_churn_predictions.csv")


print("==========================================")
print("BUSINESS INSIGHTS & RECOMMENDATIONS")
print("==========================================")


# ==========================================
# BASIC SUMMARY
# ==========================================

total_customers = len(df)

predicted_churn = (
    df["Predicted_Churn"] == "Yes"
).sum()

predicted_no_churn = (
    df["Predicted_Churn"] == "No"
).sum()


churn_rate = (
    predicted_churn / total_customers
) * 100


print("\nCUSTOMER SUMMARY")
print("------------------------------------------")

print("Total Customers:", total_customers)
print("Predicted Churn Customers:", predicted_churn)
print("Predicted Retained Customers:", predicted_no_churn)
print("Predicted Churn Rate:", round(churn_rate, 2), "%")


# ==========================================
# HIGH-RISK CUSTOMERS
# ==========================================

high_risk = df[
    df["Churn_Probability"] >= 70
]


medium_risk = df[
    (df["Churn_Probability"] >= 40) &
    (df["Churn_Probability"] < 70)
]


low_risk = df[
    df["Churn_Probability"] < 40
]


print("\nRISK SEGMENTATION")
print("------------------------------------------")

print(
    "High Risk Customers (>=70%):",
    len(high_risk)
)

print(
    "Medium Risk Customers (40%-69%):",
    len(medium_risk)
)

print(
    "Low Risk Customers (<40%):",
    len(low_risk)
)


# ==========================================
# TOP HIGH-RISK CUSTOMERS
# ==========================================

print("\nTOP 10 HIGH-RISK CUSTOMERS")
print("------------------------------------------")

print(
    high_risk
    .head(10)
    .to_string(index=False)
)


# ==========================================
# BUSINESS RECOMMENDATIONS
# ==========================================

print("\n==========================================")
print("BUSINESS RECOMMENDATIONS")
print("==========================================")


print("""
1. TARGET HIGH-RISK CUSTOMERS
   Customers with churn probability above 70%
   should receive immediate retention campaigns.

2. OFFER PERSONALIZED DISCOUNTS
   Provide targeted discounts, loyalty rewards,
   or special offers to high-risk customers.

3. IMPROVE CUSTOMER SUPPORT
   Customers showing high churn risk should receive
   proactive customer support and issue resolution.

4. MONITOR MEDIUM-RISK CUSTOMERS
   Customers with 40%-69% churn probability should
   be monitored regularly before they become high-risk.

5. CUSTOMER ENGAGEMENT
   Use personalized emails, notifications and offers
   to increase customer engagement.

6. RETENTION CAMPAIGNS
   Create targeted retention campaigns based on
   customer behaviour and service usage.

7. REGULAR CHURN MONITORING
   Run the churn prediction model regularly to
   identify newly emerging high-risk customers.
""")


# ==========================================
# SAVE BUSINESS INSIGHTS
# ==========================================

insights = pd.DataFrame({
    "Insight": [
        "Identify high-risk customers",
        "Provide personalized discounts",
        "Improve customer support",
        "Monitor medium-risk customers",
        "Increase customer engagement",
        "Run targeted retention campaigns",
        "Monitor churn regularly"
    ],
    "Recommendation": [
        "Target customers with churn probability >= 70%",
        "Offer personalized discounts and loyalty rewards",
        "Provide proactive support to high-risk customers",
        "Monitor customers with 40%-69% churn probability",
        "Use personalized communication and offers",
        "Create targeted customer retention campaigns",
        "Run the churn model periodically"
    ]
})


insights.to_csv(
    "business_insights.csv",
    index=False
)


print("\nBusiness insights saved to:")
print("business_insights.csv")

print("\nSTEP 35 COMPLETED SUCCESSFULLY!")