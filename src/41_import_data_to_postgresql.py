import os
import glob
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# =========================================================
# 1. PostgreSQL connection
# =========================================================

DB_USER = "postgres"
DB_PASSWORD = "minni@11"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "customer_churn_db"

password = quote_plus(DB_PASSWORD)

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

print("Connecting to PostgreSQL...")

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("PostgreSQL connected successfully!")
except Exception as e:
    print("PostgreSQL connection failed!")
    print(e)
    raise SystemExit


# =========================================================
# 2. Find Excel/CSV file inside data folder
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

files = []

files.extend(glob.glob(os.path.join(DATA_DIR, "*.xlsx")))
files.extend(glob.glob(os.path.join(DATA_DIR, "*.xls")))
files.extend(glob.glob(os.path.join(DATA_DIR, "*.csv")))

if not files:
    raise FileNotFoundError(
        f"No Excel/CSV file found inside:\n{DATA_DIR}"
    )

print("\nFound data file:")
for f in files:
    print(" -", os.path.basename(f))

file_path = files[0]

print("\nUsing file:", os.path.basename(file_path))


# =========================================================
# 3. Read file
# =========================================================

try:
    if file_path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

except Exception as e:
    print("Error while reading data file:")
    print(e)
    raise SystemExit


print("\nOriginal columns:")
print(df.columns.tolist())

print("\nOriginal rows:", len(df))


# =========================================================
# 4. Clean column names
# =========================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "", regex=False)
    .str.replace("_", "", regex=False)
)

print("\nCleaned columns:")
print(df.columns.tolist())


# =========================================================
# 5. Rename important columns
# =========================================================

rename_map = {
    "customerid": "customer_id",
    "customers": "customer_id",

    "seniorcitizen": "senior_citizen",
    "phoneservice": "phone_service",
    "multiplelines": "multiple_lines",
    "internetservice": "internet_service",
    "onlinesecurity": "online_security",
    "onlinebackup": "online_backup",
    "deviceprotection": "device_protection",
    "techsupport": "tech_support",
    "streamingtv": "streaming_tv",
    "streamingmovies": "streaming_movies",
    "paperlessbilling": "paperless_billing",
    "paymentmethod": "payment_method",
    "monthlycharges": "monthly_charges",
    "totalcharges": "total_charges"
}

df = df.rename(columns=rename_map)


# =========================================================
# 6. Create customer_id if missing
# =========================================================

if "customer_id" not in df.columns:
    df.insert(
        0,
        "customer_id",
        ["C" + str(i).zfill(5) for i in range(1, len(df) + 1)]
    )

else:
    df["customer_id"] = df["customer_id"].astype(str).str.strip()

    # Replace empty customer IDs
    empty_ids = (
        df["customer_id"].isna()
        | (df["customer_id"].astype(str).str.strip() == "")
    )

    df.loc[empty_ids, "customer_id"] = [
        "C" + str(i).zfill(5)
        for i in range(1, empty_ids.sum() + 1)
    ]


# =========================================================
# 7. Remove duplicate customers
# =========================================================

df = df.drop_duplicates(subset=["customer_id"])

print("\nCustomers after cleaning:", len(df))


# =========================================================
# 8. Convert numeric columns
# =========================================================

numeric_columns = [
    "senior_citizen",
    "tenure",
    "monthly_charges",
    "total_charges",
    "ltv"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


# =========================================================
# 9. Create LTV if it doesn't exist
# =========================================================

if "ltv" not in df.columns:

    print("\nLTV column not found. Creating LTV...")

    df["ltv"] = (
        df["monthly_charges"].fillna(0)
        * df["tenure"].fillna(0)
    )

else:
    df["ltv"] = df["ltv"].fillna(
        df["monthly_charges"].fillna(0)
        * df["tenure"].fillna(0)
    )


# =========================================================
# 10. Create customers table
# =========================================================

customers_df = df.copy()

# PostgreSQL doesn't need pandas index
customers_df = customers_df.reset_index(drop=True)

print("\nWriting customers table...")

customers_df.to_sql(
    "customers",
    engine,
    schema="public",
    if_exists="replace",
    index=False,
    method="multi",
    chunksize=1000
)

print("customers table inserted successfully!")


# =========================================================
# 11. Create customer_ltv_features table
# =========================================================

ltv_columns = [
    "customer_id",
    "tenure",
    "monthly_charges",
    "total_charges",
    "contract",
    "internet_service",
    "payment_method",
    "churn",
    "ltv"
]

available_ltv_columns = [
    col for col in ltv_columns
    if col in df.columns
]

ltv_df = df[available_ltv_columns].copy()

# Additional useful LTV feature
if "monthly_charges" in ltv_df.columns:
    if "tenure" in ltv_df.columns:
        ltv_df["predicted_ltv"] = (
            ltv_df["monthly_charges"].fillna(0)
            * ltv_df["tenure"].fillna(0)
        )

# Remove duplicate customers
ltv_df = ltv_df.drop_duplicates(
    subset=["customer_id"]
)

print("\nWriting customer_ltv_features table...")

ltv_df.to_sql(
    "customer_ltv_features",
    engine,
    schema="public",
    if_exists="replace",
    index=False,
    method="multi",
    chunksize=1000
)

print("customer_ltv_features table inserted successfully!")


# =========================================================
# 12. Verify row counts
# =========================================================

print("\n" + "=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

with engine.connect() as conn:

    customers_count = conn.execute(
        text("SELECT COUNT(*) FROM public.customers")
    ).scalar()

    ltv_count = conn.execute(
        text("SELECT COUNT(*) FROM public.customer_ltv_features")
    ).scalar()

print("\ncustomers rows =", customers_count)
print("customer_ltv_features rows =", ltv_count)


# =========================================================
# 13. Show sample data
# =========================================================

print("\nCustomers sample:")
print(
    pd.read_sql(
        "SELECT * FROM public.customers LIMIT 5",
        engine
    )
)

print("\nLTV features sample:")
print(
    pd.read_sql(
        "SELECT * FROM public.customer_ltv_features LIMIT 5",
        engine
    )
)


# =========================================================
# DONE
# =========================================================

print("\n" + "=" * 60)
print("SUCCESS!")
print("Both PostgreSQL tables contain data.")
print("=" * 60)