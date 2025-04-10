import psycopg2
import os


def create_test_db():
    dbname = "test_db"
    user = os.getenv("DB_USER", "user")
    password = os.getenv("DB_PASS", "password")
    host = os.getenv("DB_HOST", "db")

    conn = psycopg2.connect(dbname="notification_db", user=user, password=password, host=host)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {dbname}")
        print(f"Created database: {dbname}")
    else:
        print(f"Database '{dbname}' already exists.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    create_test_db()
