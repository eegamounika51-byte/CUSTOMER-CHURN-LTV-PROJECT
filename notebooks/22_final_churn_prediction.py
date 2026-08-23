import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_excel("data/TELCO_CHURN.CSV.xlsx")

print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))


# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = df.columns.str.strip()

print("\nDataset columns:")
print(df.columns.tolist())


# ==========================================
# CONVERT CHURN TO 0/1
# ==========================================

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ==========================================
# HANDLE CUSTOMER ID
# ==========================================

id_column = None

for column in df.columns:
   if column.lower() in ["customerid", "customer_id", "customer id", "customers"]:
        id_column = column
        break


if id_column is not None:
    customer_ids = df[id_column]
    X = df.drop(columns=["Churn", id_column])

else:
    customer_ids = pd.Series(
        range(1, len(df) + 1),
        index=df.index,
        name="CustomerID"
    )

    X = df.drop(columns=["Churn"])


y = df["Churn"]


# ==========================================
# ENCODE CATEGORICAL VARIABLES
# ==========================================

X = pd.get_dummies(
    X,
    drop_first=True
)


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

X = X.fillna(0)


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# FINAL RANDOM FOREST MODEL
# ==========================================

final_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)


final_model.fit(
    X_train,
    y_train
)


# ==========================================
# FINAL CHURN PREDICTION
# ==========================================

predictions = final_model.predict(X_test)

probabilities = final_model.predict_proba(
    X_test
)[:, 1]


# ==========================================
# CREATE PREDICTION RESULTS
# ==========================================

prediction_results = pd.DataFrame({
    "CustomerID": customer_ids.loc[X_test.index].values,
    "Actual_Churn": y_test.values,
    "Predicted_Churn": predictions,
    "Churn_Probability": probabilities
})


# ==========================================
# CONVERT 0/1 TO YES/NO
# ==========================================

prediction_results["Actual_Churn"] = (
    prediction_results["Actual_Churn"]
    .map({
        0: "No",
        1: "Yes"
    })
)


prediction_results["Predicted_Churn"] = (
    prediction_results["Predicted_Churn"]
    .map({
        0: "No",
        1: "Yes"
    })
)


# ==========================================
# ROUND CHURN PROBABILITY
# ==========================================

prediction_results["Churn_Probability"] = (
    prediction_results["Churn_Probability"] * 100
).round(2)


# ==========================================
# SORT BY CHURN PROBABILITY
# ==========================================

prediction_results = prediction_results.sort_values(
    by="Churn_Probability",
    ascending=False
)


# ==========================================
# DISPLAY TOP 20 HIGH-RISK CUSTOMERS
# ==========================================

print("\n==========================================")
print("FINAL CHURN PREDICTION")
print("==========================================")

print(
    prediction_results.head(20).to_string(
        index=False
    )
)


# ==========================================
# SAVE FINAL PREDICTIONS
# ==========================================

prediction_results.to_csv(
    "final_churn_predictions.csv",
    index=False
)


# ==========================================
# SUMMARY
# ==========================================

total_customers = len(prediction_results)

predicted_churn = (
    prediction_results["Predicted_Churn"] == "Yes"
).sum()

predicted_no_churn = (
    prediction_results["Predicted_Churn"] == "No"
).sum()


print("\n==========================================")
print("PREDICTION SUMMARY")
print("==========================================")

print("Customers Tested:", total_customers)
print("Predicted Churn:", predicted_churn)
print("Predicted No Churn:", predicted_no_churn)

print("\nFinal prediction file created:")
print("final_churn_predictions.csv")

print("\nSTEP 34 COMPLETED SUCCESSFULLY!")