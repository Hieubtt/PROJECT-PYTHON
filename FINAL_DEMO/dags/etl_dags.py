from __future__ import annotations

import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

DAG_ID = "saleFinancial_risk_assessment_to_dw"

# INGEST_SCRIPT = "/opt/airflow/dags/scripts/load_csv_to_postgres_raw.py"
# ETL_SCRIPT    = "/opt/airflow/dags/scripts/etl_sales_transform_load.py"
# CHECK_SCRIPT  = "/opt/airflow/dags/scripts/post_run_check.py"

PYTHON = "python"

default_args = {"owner": "hieubtt", "retries": 2, "retry_delay": timedelta(minutes=1)}

DB_ENV = {
    "DB_HOST": os.getenv("DB_HOST", "postgres"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_NAME": os.getenv("DB_NAME", "fin_risk_assessment_db"),
    "DB_USER": os.getenv("DB_USER", "admin"),#airflow
    "DB_PASS": os.getenv("DB_PASS", "admin"),#airflow
    "CSV_PATH": os.getenv("CSV_PATH", "/opt/airflow/dags/data/sales_raw.csv"),
}

with DAG(
    dag_id=DAG_ID,
    description="E2E demo: CSV -> Postgres(raw) -> DW using ETL + Airflow",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["demo", "sales", "etl"],
) as dag:
    start = EmptyOperator(task_id="start")

    ingest = BashOperator(
        task_id="ingest_csv_to_raw",
        bash_command=f'',
        env=DB_ENV,
    )

    transform_load = BashOperator(
        task_id="transform_load_dw",
        bash_command=f'',
        env=DB_ENV,
    )

    check = BashOperator(
        task_id="post_run_check",
        bash_command=f'',
        env=DB_ENV,
    )

    end = EmptyOperator(task_id="end")

    start >> ingest >> transform_load >> check >> end
