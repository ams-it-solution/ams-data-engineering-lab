from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG(
    dag_id='first_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    create_table = PostgresOperator(
        task_id='create_table',

        postgres_conn_id='postgres_default',

        sql="""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            country VARCHAR(100)
        );
        """
    )

    insert_data = PostgresOperator(
        task_id='insert_data',

        postgres_conn_id='postgres_default',

        sql="""
        INSERT INTO customers (name, country)
        VALUES
        ('Andre', 'Brazil'),
        ('John', 'USA');
        """
    )

    create_table >> insert_data