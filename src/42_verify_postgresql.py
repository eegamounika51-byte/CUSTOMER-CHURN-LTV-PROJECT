import psycopg2


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

print("PostgreSQL connected successfully!")


# ==========================================
# 1. TOTAL CUSTOMERS
# ==========================================

cursor.execute("""
SELECT COUNT(*)
FROM customers;
""")

total_customers = cursor.fetchone()[0]

print("\nTotal Customers:", total_customers)


# ==========================================
# 2. CHURN COUNT
# ==========================================

cursor.execute("""
SELECT churn, COUNT(*)
FROM customers
GROUP BY churn
ORDER BY churn;
""")

print("\nChurn Distribution:")

for row in cursor.fetchall():
    print(row[0], ":", row[1])


# ==========================================
# 3. AVERAGE MONTHLY CHARGES
# ==========================================

cursor.execute("""
SELECT ROUND(AVG(monthly_charges), 2)
FROM customers;
""")

average_charges = cursor.fetchone()[0]

print("\nAverage Monthly Charges:", average_charges)


# ==========================================
# 4. CONTRACT DISTRIBUTION
# ==========================================

cursor.execute("""
SELECT contract, COUNT(*)
FROM customers
GROUP BY contract
ORDER BY COUNT(*) DESC;
""")

print("\nContract Distribution:")

for row in cursor.fetchall():
    print(row[0], ":", row[1])


# ==========================================
# 5. SAMPLE CUSTOMERS
# ==========================================

cursor.execute("""
SELECT customer_id, gender, tenure,
       monthly_charges, churn
FROM customers
LIMIT 5;
""")

print("\nSample Customers:")

for row in cursor.fetchall():
    print(row)


# ==========================================
# CLOSE
# ==========================================

cursor.close()
connection.close()

print("\nPostgreSQL connection closed!")
print("\nSTEP 42 COMPLETED SUCCESSFULLY!")