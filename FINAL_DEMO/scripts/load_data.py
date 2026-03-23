from __future__ import annotations

import os
import sys
import uuid
import pandas as pd
import psycopg2

RUN_ID = f"RUN_{uuid.uuid4().hex[:8]}"


def env(name: str, default: str | None = None) -> str:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        if default is None:
            raise RuntimeError(f"Missing env var: {name}")
        return default
    return v.strip()

SQL_LOG = "INSERT INTO etl_log(run_id, step_name, status, message) VALUES (%s,%s,%s,%s);"

SQL_BUILD_STAGING = r'''
DROP TABLE IF EXISTS fin_risk_assessment;

CREATE TABLE fin_risk_assessment (
Age INT,
Gender VARCHAR(50),
Education_Level VARCHAR(50),
Marital_Status VARCHAR(50),
Income FLOAT NULL,
Credit_Score FLOAT NULL,
Loan_Amount FLOAT NULL,
Loan_Purpose  VARCHAR(50) NULL,
Employment_Status VARCHAR(50) NULL,
Years_at_Current_Job FLOAT NULL,
Payment_History VARCHAR(50) NULL,
Debt_to_Income_Ratio FLOAT NULL,
Assets_Value FLOAT NULL,
Number_of_Dependents FLOAT NULL,
City VARCHAR(250) NULL, 
State VARCHAR(2) NULL,
Country VARCHAR(250) NULL,
Previous_Defaults FLOAT NULL, 
Marital_Status_Change FLOAT NULL, 
Risk_Rating VARCHAR(50) NULL,
id SERIAL PRIMARY KEY,
load_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);
'''
SQL_BUILD_INSERT = '''
INSERT INTO fin_risk_assessment (
    Age, Gender, Education_Level, Marital_Status, Income, Credit_Score,
    Loan_Amount, Loan_Purpose, Employment_Status, Years_at_Current_Job,
    Payment_History, Debt_to_Income_Ratio, Assets_Value,
    Number_of_Dependents, City, State, Country,
    Previous_Defaults, Marital_Status_Change, Risk_Rating ,id,load_at
)
    select Age, Gender, Education_Level, Marital_Status, Income, Credit_Score,
    Loan_Amount, Loan_Purpose, Employment_Status, Years_at_Current_Job,
    Payment_History, Debt_to_Income_Ratio, Assets_Value,
    Number_of_Dependents, City, State, Country,
    Previous_Defaults, Marital_Status_Change, Risk_Rating, id ,NOW()
    from rawdata
'''
SQL_CHECK_DUPLICATE ='''
    select id,count(id) from public.fin_risk_assessment 
    group by id having count(id) > 2
'''   
#fin_risk_assessment

def log(cur, step: str, status: str, msg: str = ""):
    cur.execute(SQL_LOG, (RUN_ID, step, status, msg))


def main():
    conn = psycopg2.connect(
        host="postgres_airflow",
        port=5432,
        database="fin_etl_db",
        user="admin",   
        password="admin"
    )
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            log(cur,"LOAD","START","CHECK + CREATE TABLE fin_risk_assessment")
            cur.execute(SQL_BUILD_STAGING)
            log(cur,"LOAD","START","CHECK + CREATE TABLE fin_risk_assessment")
            
            log(cur, "LOAD", "SUCCESS", "Insert table ")
            log(cur,"VALIDATE","START","Check duplicates + counts")
            cur.execute(SQL_CHECK_DUPLICATE)
            if cur.fetchall():
                raise RuntimeError("Duplicate sale_id detected in rawdawta")
            cur.execute(SQL_BUILD_INSERT)
            conn.commit()
            print(f"ETL PASSED | RUN_ID={RUN_ID}")
    except Exception as e:
        conn.rollback()
        print(f"ETL FAILED | RUN_ID={RUN_ID} | ERROR={e}")
    finally:
        conn.close()
if __name__ == "__main__":
    main()
