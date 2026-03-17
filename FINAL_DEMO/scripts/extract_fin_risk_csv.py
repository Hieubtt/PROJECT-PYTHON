from __future__ import annotations

import os
import sys
import uuid

import psycopg2

RUN_ID = f"RUN_{uuid.uuid4().hex[:8]}"

def env(name: str, default: str | None = None) -> str:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        if default is None:
            raise RuntimeError(f"Missing env var: {name}")
        return default
    return v.strip()

DB = {
    "host": env("DB_HOST", "postgres"),
    "port": int(env("DB_PORT", "5435")),
    "database": env("DB_NAME", "fin_risk_assessment_db"),
    "user": env("DB_USER", "admin"),
    "password": env("DB_PASS", "admin"),
    "connect_timeout": int(env("DB_TIMEOUT", "10")),
}

SQL_CREATE_TABLE_LOG = '''
  CREATE TABLE ETL_LOG 
  (
    run_id INT PRIMARY KEY, 
    step_name TEXT, 
    status TEXT, 
    message TEXT
  );
  '''
# CREATE TABLE fin_risk_assessment (
# Age INT,
# Gender TEXT,
# Education_Level TEXT,
# Marital_Status TEXT,
# Income INT NULL,
# Credit_Score INT NULL,
# Loan_Amount FLOAT NULL,
# Loan_Purpose  NULL,
# Employment_Status TEXT NULL,
# Years_at_Current_Job INT,
# Payment_History TEXT NULL,
# Debt_to_Income_Ratio FLOAT NULL,
# Assets_Value TEXT,
# Number_of_Dependents INT NULL,
# City TEXT NULL, 
# State VARCHAR(2) NULL,
# Country TEXT NULL,
# Previous_Defaults TEXT NULL, 
# Marital_Status_Change TEXT NULL, 
# Risk_Rating TEXT NULL
# )

SQL_LOG = "INSERT INTO etl_log(run_id, step_name, status, message) VALUES (%s,%s,%s,%s);"

SQL_BUILD_STAGING = r'''
DROP TABLE IF EXISTS etl.sales_staging_clean;

CREATE TABLE etl.sales_staging_clean (
  sale_id        TEXT PRIMARY KEY,
  sale_date      DATE NOT NULL,
  customer_id    TEXT NOT NULL,
  product_id     TEXT NOT NULL,
  quantity       INT  NOT NULL CHECK (quantity > 0),
  unit_price     NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
  payment_method TEXT NOT NULL CHECK (payment_method IN ('cash','card','ewallet')),
  store_city     TEXT
);

WITH parsed AS (
  SELECT
    raw_id,
    NULLIF(sale_id_text,'') AS sale_id,
    CASE
      WHEN sale_date_text ~ '^\d{4}-\d{2}-\d{2}$' THEN sale_date_text::DATE
      ELSE NULL
    END AS sale_date,
    NULLIF(customer_id_text,'') AS customer_id,
    NULLIF(product_id_text,'')  AS product_id,
    CASE
      WHEN quantity_text ~ '^[-+]?[0-9]+$' THEN quantity_text::INT
      ELSE NULL
    END AS quantity,
    CASE
      WHEN unit_price_text ~ '^[-+]?[0-9]*\.?[0-9]+$' THEN unit_price_text::NUMERIC(10,2)
      ELSE NULL
    END AS unit_price,
    payment_method,
    store_city
  FROM raw.sales_raw
),
dedup AS (
  SELECT DISTINCT ON (sale_id)
    sale_id, sale_date, customer_id, product_id, quantity, unit_price, payment_method, store_city, raw_id
  FROM parsed
  WHERE sale_id IS NOT NULL
  ORDER BY sale_id, raw_id DESC
),
cleaned AS (
  SELECT sale_id, sale_date, customer_id, product_id, quantity, unit_price, payment_method, store_city
  FROM dedup
  WHERE sale_date IS NOT NULL
    AND customer_id IS NOT NULL
    AND product_id IS NOT NULL
    AND quantity IS NOT NULL AND quantity > 0
    AND unit_price IS NOT NULL AND unit_price >= 0
    AND payment_method IN ('cash','card','ewallet')
)
INSERT INTO etl.sales_staging_clean
  (sale_id, sale_date, customer_id, product_id, quantity, unit_price, payment_method, store_city)
SELECT sale_id, sale_date, customer_id, product_id, quantity, unit_price, payment_method, store_city
FROM cleaned;
'''

SQL_UPSERT_DW = '''
INSERT INTO dw.sales_fact(
  sale_id, sale_date, customer_id, product_id, quantity, unit_price, revenue, payment_method, store_city
)
SELECT
  sale_id, sale_date, customer_id, product_id, quantity, unit_price,
  (quantity * unit_price)::NUMERIC(12,2) AS revenue,
  payment_method, store_city
FROM etl.sales_staging_clean
ON CONFLICT (sale_id) DO UPDATE
SET sale_date      = EXCLUDED.sale_date,
    customer_id    = EXCLUDED.customer_id,
    product_id     = EXCLUDED.product_id,
    quantity       = EXCLUDED.quantity,
    unit_price     = EXCLUDED.unit_price,
    revenue        = EXCLUDED.revenue,
    payment_method = EXCLUDED.payment_method,
    store_city     = EXCLUDED.store_city,
    loaded_at      = NOW();
'''

SQL_VALIDATE_DUP = "SELECT sale_id, COUNT(*) FROM dw.sales_fact GROUP BY sale_id HAVING COUNT(*)>1;"
SQL_COUNT = "SELECT (SELECT COUNT(*) FROM etl.sales_staging_clean), (SELECT COUNT(*) FROM dw.sales_fact);"

def log(cur, step: str, status: str, msg: str = ""):
    cur.execute(SQL_LOG, (RUN_ID, step, status, msg))

def main():
    conn = psycopg2.connect(**DB)
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            log(cur,"PIPELINE","START","Transform + Load sales")
            log(cur,"TRANSFORM","START","Build staging")
            cur.execute(SQL_BUILD_STAGING)
            log(cur,"TRANSFORM","SUCCESS","Staging built")

            log(cur,"LOAD","START","Upsert to DW")
            cur.execute(SQL_UPSERT_DW)
            log(cur,"LOAD","SUCCESS","Upsert done")

            log(cur,"VALIDATE","START","Check duplicates + counts")
            cur.execute(SQL_VALIDATE_DUP)
            if cur.fetchall():
                raise RuntimeError("Duplicate sale_id detected in dw.sales_fact")

            cur.execute(SQL_COUNT)
            staging_cnt, dw_cnt = cur.fetchone()
            if staging_cnt <= 0:
                raise RuntimeError("staging_cnt=0 (no valid rows after cleaning)")
            log(cur,"VALIDATE","SUCCESS",f"staging_cnt={staging_cnt}, dw_cnt={dw_cnt}")

            log(cur,"PIPELINE","SUCCESS","ETL finished")
        conn.commit()
        print(f"ETL PASSED | RUN_ID={RUN_ID}")
        sys.exit(0)
    except Exception as e:
        conn.rollback()
        try:
            conn.autocommit = True
            with conn.cursor() as cur:
                log(cur,"PIPELINE","FAIL",str(e))
        except Exception:
            pass
        print(f"ETL FAILED | RUN_ID={RUN_ID} | ERROR={e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
