import time
import psycopg2
from psycopg2.extras import execute_values


def connect_db(retry=5, delay=5):
    for i in range(retry):
        try:
            conn = psycopg2.connect(
                host="postgres_airflow",
                port=5432,
                database="dvdrental",
                user="postgres",
                password="admin"
            )
            print("Ket noi database thanh cong")
            return conn
        except Exception as e:
            print(f"Retry connect DB {i+1}/{retry} ... {e}")
            time.sleep(delay)

    raise Exception("Khong the ket noi PostgreSQL")


def run_etl():

    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        print("Tao bang report_revenue neu chua ton tai")

        cur.execute("""
        CREATE TABLE IF NOT EXISTS report_revenue
        (
            category_name VARCHAR(25) PRIMARY KEY,
            total_revenue NUMERIC,
            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        print("Extract du lieu")

        query = """
        SELECT 
            c.name,
            SUM(p.amount) AS total_revenue
        FROM category c
        JOIN film_category fc ON fc.category_id = c.category_id
        JOIN inventory i ON i.film_id = fc.film_id
        JOIN rental r ON i.inventory_id = r.inventory_id
        JOIN payment p ON p.rental_id = r.rental_id
        GROUP BY c.name
        ORDER BY total_revenue DESC;
        """

        cur.execute(query)
        result = cur.fetchall()

        print(f"So dong du lieu: {len(result)}")

        print("Load du lieu vao report_revenue")

        insert_query = """
        INSERT INTO report_revenue (category_name, total_revenue)
        VALUES %s
        ON CONFLICT (category_name)
        DO UPDATE SET
            total_revenue = EXCLUDED.total_revenue,
            last_update = CURRENT_TIMESTAMP;
        """

        execute_values(cur, insert_query, result)

        conn.commit()

        print("ETL pipeline da hoan thanh")

    except Exception as e:
        raise Exception(f"ETL pipeline loi: {e}")

    finally:
        if cur:
            cur.close()

        if conn:
            conn.close()


if __name__ == "__main__":
    run_etl()
