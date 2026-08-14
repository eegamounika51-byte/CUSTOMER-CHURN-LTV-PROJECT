import psycopg2


# ==========================================
# POSTGRESQL DATABASE CONNECTION
# ==========================================

def get_connection():

    connection = psycopg2.connect(
        host="localhost",
        database="customer_churn_db",
        user="postgres",
        password="minni@11",
        port="5432"
    )

    return connection


# ==========================================
# TEST CONNECTION
# ==========================================

if __name__ == "__main__":

    try:

        connection = get_connection()

        print("PostgreSQL connection successful!")

        connection.close()

        print("Database connection closed.")

    except Exception as e:

        print("Database connection failed!")
        print("Error:", e)