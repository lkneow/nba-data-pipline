import os
import logging
import requests
import zipfile
import re


from airflow import DAG
from airflow.decorators import task, task_group
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import taskinstance

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

# import pyarrow.csv as pv
# import pyarrow.parquet as pq

GCP_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
GCS_BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'nba_pipeline_dataset')

HOME_DIR = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
DOWNLOAD_DIR = os.path.join(HOME_DIR, "tmp_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
EXTRACT_DIR = os.path.join(DOWNLOAD_DIR, "extracted_files")
os.makedirs(EXTRACT_DIR, exist_ok=True)


ZIP_FILE_URL = "https://www.kaggle.com/api/v1/datasets/download/nathanlauga/nba-games"

# Step 1: Download the ZIP file
def download_zip(**kwargs):
    
    zip_file_path = os.path.join(DOWNLOAD_DIR, "downloaded_file.zip")
    
    response = requests.get(ZIP_FILE_URL, stream=True)
    if response.status_code == 200:
        with open(zip_file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"ZIP file downloaded to {zip_file_path}")
        kwargs['ti'].xcom_push(key='zip_file_path', value=zip_file_path)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

# Step 2: Extract the ZIP file
def extract_zip(**kwargs):
    zip_file_path = kwargs['ti'].xcom_pull(key='zip_file_path', task_ids='download_zip')

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    print(f"ZIP file extracted to {EXTRACT_DIR}")
    kwargs['ti'].xcom_push(key='extract_dir', value=EXTRACT_DIR)

@task
def list_gcs_files(**kwargs):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(GCS_BUCKET)
    blobs = bucket.list_blobs()
    
    file_paths = [blob.name for blob in blobs if blob.name.endswith(".csv")]
    if not file_paths:
        raise ValueError("No CSV files found in the GCS bucket.")
    # kwargs['ti'].xcom_push(key='file_paths', value=file_paths)
    return file_paths

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'start_date': days_ago(1),  # Replace with your start date
}

# Define the DAG
with DAG(
    dag_id="data_ingestion_gcs_bigquery",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
    catchup=False,
) as dag:

    # Task to download the ZIP file
    download_task = PythonOperator(
        task_id="download_zip",
        python_callable=download_zip,
        provide_context=True,
    )

    # Task to extract the ZIP file
    extract_task = PythonOperator(
        task_id="extract_zip",
        python_callable=extract_zip,
        provide_context=True,
    )
    
    upload_to_gcs_task = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src=f"{EXTRACT_DIR}/*.csv",  # Assuming extracted files are CSV
        dst="data/",  # Specify the destination prefix inside the GCS bucket
        bucket=GCS_BUCKET,
    )
    
    @task
    def list_gcs_files(bucket_name):
        """List CSV files in GCS bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs()

        # Collect CSV file paths
        file_list = [blob.name for blob in blobs if blob.name.endswith(".csv")]
        if not file_list:
            raise ValueError("No CSV files found in GCS.")
        return file_list
    
    gcs_files = list_gcs_files(bucket_name=GCS_BUCKET)
        
    # example from https://github.com/astronomer/webinar-task-groups/blob/main/dags/task_group_mapping_use_case.py
    @task_group(group_id="get_table_name_and_load_to_bq")
    def get_table_name_and_load_to_bq(file_name):
        @task
        def generate_table_name(file_name: str) -> str:
            """Generates sanitized BigQuery table names from GCS file names."""
            table_name = re.sub(r"[^a-zA-Z0-9_]", "_", file_name.split("/")[-1].replace(".csv", ""))
            final_table_names=f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{table_name}"
            return final_table_names

        table_name = generate_table_name(file_name)
        
        load_to_bq = GCSToBigQueryOperator(
            task_id="load_csv_to_bq",
            bucket=GCS_BUCKET,
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            autodetect=True,
            source_objects=[file_name],
            destination_project_dataset_table=table_name
        )
        
        table_name >> load_to_bq
    tg_object = get_table_name_and_load_to_bq.expand(file_name=gcs_files)
    # Define task dependencies
    download_task >> extract_task >> upload_to_gcs_task >> gcs_files >> tg_object