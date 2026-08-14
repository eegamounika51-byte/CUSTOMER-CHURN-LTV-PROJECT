import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DB_USER = "postgres"
DB_PASSWORD = "minni@11"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "customer_churn_db"


# ==========================================
# CREATE SQLALCHEMY CONNECTION
# ==========================================

encoded_password = quote_plus(DB_PASSWORD)

connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{encoded_password}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)

print("SQLAlchemy engine created successfully!")


# ==========================================
# TEST CONNECTION
# ==========================================

try:

    with engine.connect() as connection:

        connection.execute(
            __import__("sqlalchemy").text("SELECT 1")
        )

    print("PostgreSQL connection successful!")

except Exception as e:

    print("PostgreSQL connection failed!")
    print(e)
    raise


# ==========================================
# LOAD CUSTOMER DATA
# ==========================================

query = """
SELECT
    customer_id,
    tenure,
    monthly_charges,
    total_charges,
    contract,
    internet_service,
    churn
FROM customers;
"""

df = pd.read_sql(query, engine)

print("\nCustomer data loaded successfully!")
print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# DATA CLEANING
# ==========================================

df["monthly_charges"] = pd.to_numeric(
    df["monthly_charges"],
    errors="coerce"
).fillna(0)

df["total_charges"] = pd.to_numeric(
    df["total_charges"],
    errors="coerce"
).fillna(0)

df["tenure"] = pd.to_numeric(
    df["tenure"],
    errors="coerce"
).fillna(0)


# ==========================================
# FEATURE 1 — MONTHLY REVENUE
# ==========================================

df["monthly_revenue"] = df["monthly_charges"]


# ==========================================
# FEATURE 2 — ESTIMATED LIFESPAN
# ==========================================

df["estimated_lifespan"] = df["tenure"].apply(
    lambda x: max(x, 1)
)


# ==========================================
# FEATURE 3 — BASIC LTV
# ==========================================

df["ltv"] = (
    df["monthly_charges"]
    * df["estimated_lifespan"]
)


# ==========================================
# FEATURE 4 — REVENUE PER MONTH
# ==========================================

df["revenue_per_month"] = (
    df["total_charges"]
    / df["estimated_lifespan"]
)


# ==========================================
# FEATURE 5 — LTV SEGMENT
# ==========================================

df["ltv_segment"] = pd.cut(
    df["ltv"],
    bins=[
        -1,
        1000,
        3000,
        6000,
        float("inf")
    ],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "Very High Value"
    ]
)


# ==========================================
# DISPLAY LTV FEATURES
# ==========================================

print("\n==========================================")
print("LTV FEATURES")
print("==========================================")

print(
    df[
        [
            "customer_id",
            "tenure",
            "monthly_charges",
            "total_charges",
            "ltv",
            "ltv_segment"
        ]
    ].head(10)
)


# ==========================================
# LTV STATISTICS
# ==========================================

print("\n==========================================")
print("LTV STATISTICS")
print("==========================================")

print(df["ltv"].describe())


# ==========================================
# LTV SEGMENT DISTRIBUTION
# ==========================================

print("\n==========================================")
print("LTV SEGMENT DISTRIBUTION")
print("==========================================")

print(
    df["ltv_segment"].value_counts()
)


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

import os

os.makedirs("outputs", exist_ok=True)


# ==========================================
# SAVE CSV
# ==========================================

output_file = "outputs/ltv_features.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nLTV features saved successfully:")
print(output_file)


# ==========================================
# SAVE TO POSTGRESQL
# ==========================================

df.to_sql(
    "customer_ltv_features",
    engine,
    if_exists="replace",
    index=False
)

print("\nLTV data stored in PostgreSQL!")
print("Table: customer_ltv_features")


# ==========================================
# VERIFY POSTGRESQL TABLE
# ==========================================

verify_query = """
SELECT COUNT(*)
FROM customer_ltv_features;
"""

verify_df = pd.read_sql(
    verify_query,
    engine
)

print("\nRows stored in PostgreSQL:")

print(
    verify_df.iloc[0, 0]
)


# ==========================================
# FINAL MESSAGE
# ==========================================

print("\n==========================================")
print("STEP 42 COMPLETED SUCCESSFULLY!")
print("==========================================")