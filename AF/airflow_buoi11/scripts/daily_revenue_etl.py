import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

def run_etl():

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="dvdrental",
            user="postgres",
            password="admin"
        )

        cur = conn.cursor()
        conn.autocommit = True

        print("Tao bang report")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS report_revenue
            (
                category_name VARCHAR(25) PRIMARY KEY,
                total_revenue NUMERIC,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("Extract data")

        query = """
            SELECT c.name, SUM(p.amount) as total_revenue
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

        print("Load data vao table report")

        insert_query = """
        INSERT INTO report_revenue (category_name, total_revenue)
        VALUES %s
        ON CONFLICT (category_name) DO UPDATE SET
        total_revenue = EXCLUDED.total_revenue,
        last_update = CURRENT_TIMESTAMP;
        """

        execute_values(cur, insert_query, result)

        print("ETL pipeline da hoan thanh")

    except Exception as e:
        print(f"Da co loi xay ra: {e}")

    finally:
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()

if __name__ == "__main__":
    run_etl()
