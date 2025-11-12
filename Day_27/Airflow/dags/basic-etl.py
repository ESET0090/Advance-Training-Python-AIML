from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context
 
default_args = {
    'owner': 'Pankaj_Kumar',
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'email_on_failure': False,
}
 
with DAG(
    dag_id='sample_etl_dag',
    default_args=default_args,
    description='A simple ETL pipeline example',
    start_date=datetime(2025, 11, 10),
    schedule='0 9 * * *',
    catchup=False,
    tags=['example', 'etl', 'training'],
) as dag:
 
    def extract_data():
        data = ["apple", "banana", "cherry"]
        print(" Extracted data:", data)
        return data
 
    def transform_data():
        context = get_current_context()
        extracted_data = context['ti'].xcom_pull(task_ids='extract_task')
        transformed_data = [item.upper() for item in extracted_data]
        print(" Transformed data:", transformed_data)
        return transformed_data
 
    def load_data():
        context = get_current_context()
        transformed_data = context['ti'].xcom_pull(task_ids='transform_task')
        print(" Loaded data:", transformed_data)
 
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
    )
 
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
    )
 
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data,
    )
 
    extract_task >> transform_task >> load_task