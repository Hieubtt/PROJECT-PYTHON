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

DB = {
    "host": os.getenv("DB_HOST", "fin_risk_assessment_db"),
    "port": os.getenv("DB_PORT", "5435"),
    "database": os.getenv("DB_NAME", "fin_etl_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASS", "admin"),
}

SQL_CREATE_DATABASE = '''
  CREATE DATABASE IF NOT EXISTS fin_etl_db;
  '''
SQL_CREATE_TABLE_JOB = '''

CREATE TABLE IF NOT EXISTS etl_log(run_id TEXT, step_name TEXT, status TEXT, message TEXT, message TEXT) ;
'''



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
Risk_Rating VARCHAR(50) NULL
);
'''
# pf = pd.read_csv(r'C:\Users\TrungHieu\Documents\GitHub\PROJECT-PYTHON\FINAL_DEMO\data\Financial_risk_assessment.csv')
pf = pd.read_csv('/opt/airflow/data/Financial_risk_assessment.csv')
SQL_BUILD = """
INSERT INTO fin_risk_assessment (
    Age, Gender, Education_Level, Marital_Status, Income, Credit_Score,
    Loan_Amount, Loan_Purpose, Employment_Status, Years_at_Current_Job,
    Payment_History, Debt_to_Income_Ratio, Assets_Value,
    Number_of_Dependents, City, State, Country,
    Previous_Defaults, Marital_Status_Change, Risk_Rating
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
# conn = psycopg2.connect(**DB)
# conn.autocommit = False
# cur = conn.cursor()
i = 0
a=0
while i < len(pf):
  row = pf.iloc[i]
  values = (
  float(row['Age']) if row['Age'] is not None else None,
  str(row['Gender']) if row['Gender'] is not None else None,
  str(row['Education Level']) if row['Education Level'] is not None else None,
  str(row['Marital Status']) if row['Marital Status'] is not None else None,
  float(row['Income']) if row['Income'] is not None else None,
  float(row['Credit Score']) if row['Credit Score'] is not None else None,
  float(row['Loan Amount']) if row['Loan Amount'] is not None else None,
  str(row['Loan Purpose']) if row['Loan Purpose'] is not None else None,
  str(row['Employment Status']) if row['Employment Status'] is not None else None,
  float(row['Years at Current Job']) if row['Years at Current Job'] is not None else None,
  str(row['Payment History']) if row['Payment History'] is not None else None,
  float(row['Debt-to-Income Ratio']) if row['Debt-to-Income Ratio'] is not None else None,
  float(row['Assets Value']) if row['Assets Value'] is not None else None,
  float(row['Number of Dependents']) if row['Number of Dependents'] is not None else None,
  str(row['City']) if row['City'] is not None else None,
  str(row['State']) if row['State'] is not None else None,
  str(row['Country']) if row['Country'] is not None else None,
  float(row['Previous Defaults']) if row['Previous Defaults'] is not None else None,
  float(row['Marital Status Change']) if row['Marital Status Change'] is not None else None,
  str(row['Risk Rating']) if row['Risk Rating'] is not None else None
)
  #print(values)
  if i % 1000 == 0: 
    a += 1
    print(f'Đã chạy được lần {a} 1000 dòng dữ liệu và hiện đang tiếp tục ...')
  # if i == len(pf): 
  #   print('Đã hoàn thành việc insert dữ liệu .')  
  # cur.execute(SQL_BUILD, values)

  i += 1

#SQL_VALIDATE_DUP = "SELECT sale_id, COUNT(*) FROM fin_risk_assessment" # chưa can su dung nen de vay
#SQL_COUNT = "SELECT (SELECT COUNT(*) FROM etl.sales_staging_clean), (SELECT COUNT(*) FROM dw.sales_fact);"

def log(cur, step: str, status: str, msg: str = ""):
    cur.execute(SQL_LOG, (RUN_ID, step, status, msg))

def main():
    conn = psycopg2.connect(**DB)
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            cur.execute(SQL_CREATE_DATABASE)
            cur.execute(SQL_CREATE_TABLE_JOB)
            log(cur,"PIPELINE","START","Transform + Load sales")
            log(cur,"TRANSFORM","START","Build staging")
            cur.execute(SQL_BUILD_STAGING)
            
            data = []

            data = [tuple(row) for _, row in pf.iterrows()] # dung cho ten cot csv trung voi ten cot db
            cur.executemany(SQL_BUILD, data)  # insert tung dòng data 
            # cur.execute(SQL_CREATE_TABLE_LOG)
            # log(cur,"TRANSFORM","SUCCESS","Staging built")
            
            log(cur,"TRANSFORM","SUCCESS","Staging built")

            # log(cur,"LOAD","START","Upsert to DW")
            # cur.execute(SQL_UPSERT_DW)
            # log(cur,"LOAD","SUCCESS","Upsert done")

            # log(cur,"VALIDATE","START","Check duplicates + counts")
            # cur.execute(SQL_VALIDATE_DUP)
            # if cur.fetchall():
            #     raise RuntimeError("Duplicate sale_id detected in dw.postgres")

            # # cur.execute(SQL_COUNT)
            # staging_cnt, dw_cnt = cur.fetchone()
            # if staging_cnt <= 0:
            #     raise RuntimeError("staging_cnt=0 (no valid rows after cleaning)")
            # log(cur,"VALIDATE","SUCCESS",f"staging_cnt={staging_cnt}, dw_cnt={dw_cnt}")

            # log(cur,"PIPELINE","SUCCESS","ETL finished")
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
