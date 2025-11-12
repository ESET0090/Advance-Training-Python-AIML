from datetime import datetime, timedelta
import pandas as pd
import os
import requests
from io import StringIO
import logging
from pathlib import Path
import psycopg2
from psycopg2 import sql
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.hooks.base import BaseHook

# Configuration
DAG_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = str(DAG_DIR / "titanic_etl_output")  
DATASET_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

DEFAULT_ARGS = {
    'owner': 'Gaurav_Sonawane',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email_on_failure': False,
}

LOGGER = logging.getLogger(__name__)

# ============ HELPER FUNCTIONS ============

def get_pg_config_from_conn(conn_id: str = "titanic_postgres") -> dict:
    """Build psycopg2 kwargs from an Airflow Postgres connection."""
    conn = BaseHook.get_connection(conn_id)
    db = conn.schema or (conn.extra_dejson.get("database") if conn.extra_dejson else None)
    return {
        "host": conn.host or "localhost",
        "port": int(conn.port) if conn.port else 5432,
        "database": db or "postgres",
        "user": conn.login,
        "password": conn.password,
    }

def fetch_data(url: str) -> pd.DataFrame:
    """Download dataset from URL."""
    try:
        LOGGER.info(f"📥 Downloading from: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        LOGGER.info(f"✅ Extracted {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        LOGGER.error(f"❌ Fetch failed: {str(e)}")
        raise

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data and engineer features."""
    try:
        LOGGER.info(f"🔄 Transforming {len(df)} rows...")
        df = df.copy()
        
        # Fill missing values
        numeric_cols = df.select_dtypes(include=['float64']).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if df[col].isnull().any():
                df[col].fillna('Unknown', inplace=True)
        
        # Title engineering
        if 'Name' in df.columns:
            title_map = {
                'Mlle': 'Miss', 'Ms': 'Miss', 'Mme': 'Mrs',
                'Capt': 'Officer', 'Col': 'Officer', 'Major': 'Officer',
                'Dr': 'Officer', 'Rev': 'Officer', 'Don': 'Royalty',
                'Dona': 'Royalty', 'Sir': 'Royalty', 'Lady': 'Royalty',
                'Countess': 'Royalty', 'Jonkheer': 'Royalty'
            }
            df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
            df['Title'] = df['Title'].replace(title_map)
            df['Title'] = df['Title'].apply(
                lambda x: x if x in ['Mr', 'Miss', 'Mrs', 'Master', 'Officer', 'Royalty'] else 'Rare'
            )
        
        # Feature engineering
        if all(col in df.columns for col in ['SibSp', 'Parch']):
            df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
            df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        
        if 'Age' in df.columns:
            df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100],
                                    labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
        
        if 'Fare' in df.columns:
            df['FareGroup'] = pd.qcut(df['Fare'], q=4, duplicates='drop',
                                      labels=['Low', 'Medium', 'High', 'Very High'])
        
        if 'Cabin' in df.columns:
            df['Deck'] = df['Cabin'].str[0].fillna('Unknown')
        
        df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        LOGGER.info(f"✅ Transformation done. Shape: {df.shape}")
        return df
        
    except Exception as e:
        LOGGER.error(f"❌ Transform failed: {str(e)}")
        raise

def save_to_postgres_and_csv(df: pd.DataFrame, base_dir: str, pg_conn_id: str = "titanic_postgres") -> dict:
    """Save processed data to Postgres and CSV using psycopg2."""
    try:
        pg_config = get_pg_config_from_conn(pg_conn_id)
        os.makedirs(base_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save CSV locally
        csv_path = os.path.join(base_dir, f"titanic_processed_{timestamp}.csv")
        df.to_csv(csv_path, index=False)
        LOGGER.info(f"✅ CSV saved: {csv_path}")
        
        # Connect to Postgres and load data
        LOGGER.info(f"Connecting to Postgres at {pg_config['host']}:{pg_config['port']}")
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        table_name = "titanic_processed"
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            {', '.join([f'{col} TEXT' for col in df.columns])}
        );
        """
        cursor.execute(create_table_sql)
        
        # Insert data
        insert_sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
        for _, row in df.iterrows():
            cursor.execute(insert_sql, tuple(row))
        
        conn.commit()
        LOGGER.info(f"✅ {len(df)} records inserted into {table_name}")
        cursor.close()
        conn.close()
        
        return {'csv_path': csv_path, 'postgres_host': pg_config['host'], 'table_name': table_name, 'rows_inserted': len(df)}
    except Exception as e:
        LOGGER.error(f"❌ Save failed: {str(e)}")
        raise

# ============ AIRFLOW TASKS ============

def extract_task(ti):
    """TASK 1: Extract data from URL"""
    try:
        df = fetch_data(DATASET_URL)
        ti.xcom_push(key='extracted_data', value=df.to_json(orient='records'))
        LOGGER.info(f"📦 Extract complete: {df.shape}")
        return f"✅ Extract: {len(df)} records"
    except Exception as e:
        LOGGER.error(f"❌ Extract failed: {str(e)}")
        raise

def transform_task(ti):
    """TASK 2: Transform data"""
    try:
        extracted_json = ti.xcom_pull(task_ids='data_extraction', key='extracted_data')
        df = pd.read_json(StringIO(extracted_json), orient='records')
        df = clean_and_transform(df)
        ti.xcom_push(key='transformed_data', value=df.to_json(orient='records'))
        LOGGER.info(f"🔄 Transform complete: {df.shape}")
        return f"✅ Transform: {len(df)} records"
    except Exception as e:
        LOGGER.error(f"❌ Transform failed: {str(e)}")
        raise

def load_task(ti):
    """TASK 3: Save to Postgres and CSV"""
    try:
        transformed_json = ti.xcom_pull(task_ids='data_transformation', key='transformed_data')
        df = pd.read_json(StringIO(transformed_json), orient='records')
        result = save_to_postgres_and_csv(df, OUTPUT_DIR, pg_conn_id="titanic_postgres")
        ti.xcom_push(key='output_file', value=result)
        LOGGER.info(f"💾 Load complete: {result}")
        return f"✅ Load: Saved to Postgres and CSV"
    except Exception as e:
        LOGGER.error(f"❌ Load failed: {str(e)}")
        raise

def verify_task(ti):
    """TASK 4: Verify data in Postgres"""
    try:
        pg_config = get_pg_config_from_conn("titanic_postgres")
        LOGGER.info(f"Connecting to Postgres at {pg_config['host']}:{pg_config['port']}")
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor()
        
        # Query record count
        cursor.execute("SELECT COUNT(*) FROM titanic_processed;")
        total_records = cursor.fetchone()[0]
        
        LOGGER.info(f"✅ Found {total_records} records in titanic_processed table")
        cursor.close()
        conn.close()
        
        return f"✅ Verification: {total_records} records in Postgres"
    except Exception as e:
        LOGGER.error(f"❌ Verification failed: {str(e)}")
        raise    

# ============ DAG DEFINITION ============

with DAG(
    dag_id='titanic_etl_pipeline',
    default_args=DEFAULT_ARGS,
    description='Titanic ETL Pipeline with Postgres Integration (Docker to Host)',
    schedule = timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'titanic', 'postgres'],
) as dag:
    
    start = EmptyOperator(task_id='start')
    extract = PythonOperator(task_id='data_extraction', python_callable=extract_task)
    transform = PythonOperator(task_id='data_transformation', python_callable=transform_task)
    load = PythonOperator(task_id='data_loading', python_callable=load_task)
    verify = PythonOperator(task_id='data_verification', python_callable=verify_task)
    end = EmptyOperator(task_id='end')
    
    start >> extract >> transform >> load >> verify >> end