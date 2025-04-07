import psycopg2
import os


def create_test_db():
    dbname = "test_db"
    user = os.getenv("POSTGRES_USER", "user")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    host = os.getenv("POSTGRES_HOST", "db")

    conn = psycopg2.connect(dbname="postgres", user=user, password=password, host=host)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {dbname}")
        print(f"✅ Created database: {dbname}")
    else:
        print(f"ℹ️ Database '{dbname}' already exists.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    create_test_db()
