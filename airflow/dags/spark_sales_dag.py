from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="spark_sales_etl",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    run_spark_job = BashOperator(
        task_id="run_spark_job",
        bash_command="""
        docker exec pyspark python /app/spark_jobs/sales_etl.py
        """
    )


    run_spark_job