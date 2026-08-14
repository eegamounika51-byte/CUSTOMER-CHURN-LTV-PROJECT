import psycopg2


# ==========================================
# POSTGRESQL CONNECTION
# ==========================================

connection = psycopg2.connect(
    host="localhost",
    database="customer_churn_db",
    user="postgres",
    password="minni@11",
    port="5432"
)

cursor = connection.cursor()

print("PostgreSQL connected successfully!")


# ==========================================
# 1. OVERALL CHURN RATE
# ==========================================

cursor.execute("""
SELECT
    ROUND(
        100.0 * SUM(
            CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END
        ) / COUNT(*),
        2
    )
FROM customers;
""")

churn_rate = cursor.fetchone()[0]

print("\n1. Overall Churn Rate:", churn_rate, "%")


# ==========================================
# 2. CHURN BY CONTRACT
# ==========================================

cursor.execute("""
SELECT
    contract,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned
FROM customers
GROUP BY contract
ORDER BY churned DESC;
""")

print("\n2. Churn by Contract")

for row in cursor.fetchall():
    print(row)


# ==========================================
# 3. CHURN BY INTERNET SERVICE
# ==========================================

cursor.execute("""
SELECT
    internet_service,
    COUNT(*) AS customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned
FROM customers
GROUP BY internet_service
ORDER BY churned DESC;
""")

print("\n3. Churn by Internet Service")

for row in cursor.fetchall():
    print(row)


# ==========================================
# 4. HIGH MONTHLY CHARGES CUSTOMERS
# ==========================================

cursor.execute("""
SELECT
    customer_id,
    monthly_charges,
    contract,
    churn
FROM customers
WHERE monthly_charges > 80
ORDER BY monthly_charges DESC
LIMIT 10;
""")

print("\n4. High Monthly Charges Customers")

for row in cursor.fetchall():
    print(row)


# ==========================================
# 5. HIGH-RISK CUSTOMERS
# ==========================================

cursor.execute("""
SELECT
    customer_id,
    tenure,
    monthly_charges,
    contract,
    internet_service,
    churn
FROM customers
WHERE churn = 'Yes'
  AND tenure < 12
  AND monthly_charges > 70
ORDER BY monthly_charges DESC
LIMIT 10;
""")

print("\n5. High-Risk Customers")

for row in cursor.fetchall():
    print(row)


# ==========================================
# 6. CHURN BY TENURE GROUP
# ==========================================

cursor.execute("""
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 Months'
        WHEN tenure <= 24 THEN '13-24 Months'
        WHEN tenure <= 48 THEN '25-48 Months'
        ELSE '49+ Months'
    END AS tenure_group,

    COUNT(*) AS customers,

    SUM(
        CASE WHEN churn = 'Yes'
        THEN 1 ELSE 0 END
    ) AS churned

FROM customers

GROUP BY tenure_group

ORDER BY tenure_group;
""")

print("\n6. Churn by Tenure Group")

for row in cursor.fetchall():
    print(row)


# ==========================================
# 7. AVERAGE MONTHLY CHARGES
# ==========================================

cursor.execute("""
SELECT
    churn,
    ROUND(AVG(monthly_charges), 2)
FROM customers
GROUP BY churn;
""")

print("\n7. Average Monthly Charges by Churn")

for row in cursor.fetchall():
    print(row)


# ==========================================
# CLOSE CONNECTION
# ==========================================

cursor.close()
connection.close()

print("\nPostgreSQL connection closed!")

print("\nSTEP 43 COMPLETED SUCCESSFULLY!")