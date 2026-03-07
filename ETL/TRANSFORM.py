import psycopg2
import uuid

# Cấu hình DB
DB_CONFIG = {
    "host": "localhost", # IP 10.14.29.138 
    "port": 5432,
    "database": "dvdrental", # Sử dụng DB dvdrental
    "user": "postgres",
    "password": "admin"
}

def log_step(cur, step_name: str, status: str, message: str = None) -> None:
    sql_log = """
        INSERT INTO etl_log(run_id, step_name, status, message)
        VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql_log, (RUN_ID, step_name, status, message))

cur = None
# try:
log_step(cur, "PIPELINE", "START", "Begin ETL run")
log_step(cur, "LOAD_WAREHOUSE", "START", "Upsert cleaned data into warehouse_rental")
# Transform & Load kết hợp bằng CTE
sql_load = """
    WITH cleaned AS (
        SELECT DISTINCT ON (rental_id)
            rental_id, rental_date, inventory_id, customer_id, return_date
        FROM rental
        WHERE customer_id IS NOT NULL 
            AND rental_date IS NOT NULL
        ORDER BY rental_id
    )
    INSERT INTO warehouse_rental(rental_id, rental_date, inventory_id, customer_id, return_date)
    SELECT rental_id, rental_date, inventory_id, customer_id, return_date
    FROM cleaned
    ON CONFLICT (rental_id) DO UPDATE
    SET return_date = EXCLUDED.return_date,
        loaded_at = NOW();
"""
cur.execute(sql_load)

log_step(cur, "LOAD_WAREHOUSE", "SUCCESS", "Upsert completed")
print("Load step executed. BUT not committed yet!")