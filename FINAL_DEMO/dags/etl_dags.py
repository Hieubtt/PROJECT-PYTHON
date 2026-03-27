from __future__ import annotations

import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

DAG_ID = "Financial_risk_assessment_to_dw"

# INGEST_SCRIPT = "/opt/airflow/dags/scripts/load_csv_to_postgres_raw.py"
ETL_SCRIPT    = "/opt/airflow/scripts/extract_fin_risk_csv.py"
TRANSFORM_SCRIPT    = "/opt/airflow/scripts/clean_data_fin.py"
LOAD_SCRIPT = "/opt/airflow/scripts/load_data.py"
ML_SCIPRT = "/opt/airflow/scripts/train_risk_model.py"
EMAIL_RISK_FIN = "/opt/airflow/scripts/Mail_Risk_Score.py"
# CHECK_SCRIPT  = "/opt/airflow/dags/scripts/post_run_check.py"

PYTHON = "python"

default_args = {"owner": "hieubtt", "retries": 2, "retry_delay": timedelta(minutes=1)}

DB_ENV = {
    "DB_HOST": os.getenv("DB_HOST", "localhost"), #postgres_airflow mai check lai cho nay
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_NAME": os.getenv("DB_NAME", "fin_etl_db"),
    "DB_USER": os.getenv("DB_USER", "admin"),
    "DB_PASS": os.getenv("DB_PASS", "admin")
}

with DAG(
    dag_id=DAG_ID,
    description="CSV -> Postgres ETL",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")

    etl = BashOperator(
        task_id="run_etl",
        bash_command=f'{PYTHON} {ETL_SCRIPT}',
        env=DB_ENV,
    )
    clean_data = BashOperator(
        task_id="run_clean_data",
        bash_command=f'{PYTHON} {TRANSFORM_SCRIPT}',
        env=DB_ENV,
    )
    load_data = BashOperator(
        task_id="run_load_data",
        bash_command=f'{PYTHON} {LOAD_SCRIPT}',
        env=DB_ENV,
    )
    
    ml_risk_data = BashOperator(
        task_id="run_ml_risk_data",
        bash_command=f'{PYTHON} {ML_SCIPRT}',
        env=DB_ENV,
    )

    mail_risk_data = BashOperator(
        task_id="run_mail_risk_data",
        bash_command=f'{PYTHON} {EMAIL_RISK_FIN}',
        env=DB_ENV,
    )
    end = EmptyOperator(task_id="end")

    start >> etl >> clean_data >> load_data >> ml_risk_data >> mail_risk_data >> end
