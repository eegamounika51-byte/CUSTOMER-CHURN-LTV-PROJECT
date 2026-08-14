import pandas as pd
import psycopg2


# ==========================================
# LOAD FINAL CHURN PREDICTIONS
# ==========================================

file_path = "final_churn_predictions.csv"

df = pd.read_csv(file_path)

print("Prediction file loaded successfully!")
print("Rows:", len(df))

print("\nAvailable columns:")
print(df.columns.tolist())


# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

df.columns = df.columns.str.strip()

print("\nCleaned columns:")
print(df.columns.tolist())


# ==========================================
# FIND CUSTOMER COLUMN
# ==========================================

if "customer" in df.columns:
    customer_column = "customer"

elif "customerID" in df.columns:
    customer_column = "customerID"

elif "customer_id" in df.columns:
    customer_column = "customer_id"

else:
    raise ValueError(
        "Customer ID column not found in prediction file."
    )


# ==========================================
# FIND ACTUAL CHURN COLUMN
# ==========================================

if "Churn" in df.columns:
    actual_churn_column = "Churn"

elif "actual_churn" in df.columns:
    actual_churn_column = "actual_churn"

else:
    actual_churn_column = None


# ==========================================
# FIND PREDICTED CHURN COLUMN
# ==========================================

if "Predicted_Churn" in df.columns:
    predicted_churn_column = "Predicted_Churn"

elif "predicted_churn" in df.columns:
    predicted_churn_column = "predicted_churn"

elif "Prediction" in df.columns:
    predicted_churn_column = "Prediction"

else:
    raise ValueError(
        "Predicted churn column not found."
    )


# ==========================================
# FIND CHURN PROBABILITY COLUMN
# ==========================================

if "Churn_Probability" in df.columns:
    probability_column = "Churn_Probability"

elif "churn_probability" in df.columns:
    probability_column = "churn_probability"

elif "Probability" in df.columns:
    probability_column = "Probability"

else:
    raise ValueError(
        "Churn probability column not found."
    )


print("\nDetected columns:")

print("Customer ID:",
      customer_column)

print("Actual Churn:",
      actual_churn_column)

print("Predicted Churn:",
      predicted_churn_column)

print("Probability:",
      probability_column)


# ==========================================
# CONNECT TO POSTGRESQL
# ==========================================

connection = psycopg2.connect(
    host="localhost",
    database="customer_churn_db",
    user="postgres",
    password="minni@11",
    port="5432"
)

cursor = connection.cursor()

print("\nPostgreSQL connected successfully!")


# ==========================================
# CREATE PREDICTIONS TABLE
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS churn_predictions (
    customer_id VARCHAR(50) PRIMARY KEY,
    actual_churn VARCHAR(10),
    predicted_churn VARCHAR(10),
    churn_probability NUMERIC(10,6)
);
""")

connection.commit()

print("Churn predictions table created successfully!")


# ==========================================
# INSERT QUERY
# ==========================================

insert_query = """
INSERT INTO churn_predictions (
    customer_id,
    actual_churn,
    predicted_churn,
    churn_probability
)
VALUES (%s, %s, %s, %s)

ON CONFLICT (customer_id)
DO UPDATE SET
    actual_churn =
        EXCLUDED.actual_churn,

    predicted_churn =
        EXCLUDED.predicted_churn,

    churn_probability =
        EXCLUDED.churn_probability;
"""


# ==========================================
# INSERT PREDICTIONS
# ==========================================

for _, row in df.iterrows():

    customer_id = str(
        row[customer_column]
    )

    # Actual churn
    if actual_churn_column is not None:

        actual_churn = str(
            row[actual_churn_column]
        )

    else:

        actual_churn = "Unknown"


    # Predicted churn
    predicted_churn = str(
        row[predicted_churn_column]
    )


    # Churn probability
    churn_probability = float(
        row[probability_column]
    )


    cursor.execute(
        insert_query,
        (
            customer_id,
            actual_churn,
            predicted_churn,
            churn_probability
        )
    )


# ==========================================
# COMMIT
# ==========================================

connection.commit()

print("\nPrediction data imported successfully!")


# ==========================================
# VERIFY TOTAL RECORDS
# ==========================================

cursor.execute("""
SELECT COUNT(*)
FROM churn_predictions;
""")

total_records = cursor.fetchone()[0]

print(
    "Predictions stored in PostgreSQL:",
    total_records
)


# ==========================================
# HIGH-RISK CUSTOMERS
# ==========================================

cursor.execute("""
SELECT
    customer_id,
    predicted_churn,
    churn_probability

FROM churn_predictions

WHERE predicted_churn = 'Yes'

ORDER BY churn_probability DESC

LIMIT 10;
""")


high_risk = cursor.fetchall()


print("\n==========================================")
print("TOP 10 HIGH-RISK CUSTOMERS")
print("==========================================")


if len(high_risk) == 0:

    print("No high-risk customers found.")

else:

    for row in high_risk:
        print(
            "Customer:",
            row[0],
            "| Prediction:",
            row[1],
            "| Probability:",
            row[2]
        )


# ==========================================
# CHURN SUMMARY
# ==========================================

cursor.execute("""
SELECT
    predicted_churn,
    COUNT(*)

FROM churn_predictions

GROUP BY predicted_churn

ORDER BY predicted_churn;
""")


summary = cursor.fetchall()


print("\n==========================================")
print("PREDICTION SUMMARY")
print("==========================================")


for row in summary:

    print(
        row[0],
        ":",
        row[1]
    )


# ==========================================
# CLOSE DATABASE
# ==========================================

cursor.close()

connection.close()

print("\nPostgreSQL connection closed!")

print("\n==========================================")
print("STEP 44 COMPLETED SUCCESSFULLY!")
print("==========================================")