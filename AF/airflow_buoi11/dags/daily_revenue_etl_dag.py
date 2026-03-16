from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {    
    'owner': 'data_engineer_hieubtt',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2, #nếu có có thì chạy thêm 1 lần nữa còn nếu chạy lần đầu thành công thì ko chạy nữa
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='daily_revenue_etl_dag',
    default_args=default_args,
    description='A DAG to run daily revenue ETL script',
    schedule_interval='@daily',  
    start_date=datetime(2026,3,16),
    catchup=False,
    tags=['etl', 'daily_revenue']
) as dag:

    task_start = EmptyOperator(task_id='start_pipeline')

    task_run_etl = BashOperator(
        task_id='run_daily_revenue_etl',
        bash_command='python /opt/airflow/scripts/daily_revenue_etl.py'
    )

    task_end = EmptyOperator(task_id='end_task')

    # Theo doi qui trinh chay
    task_start >> task_run_etl >> task_end
