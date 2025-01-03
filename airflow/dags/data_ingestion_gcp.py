import os
import pendulum
import requests
import zipfile
import re

from airflow.decorators import dag, task, task_group

from google.cloud import storage
from airflow.providers.google.cloud.transfers.local_to_gcs import (
    LocalFilesystemToGCSOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_GCS_DATA_BUCKET = os.environ.get("GCP_GCS_DATA_BUCKET")
BIGQUERY_DATASET_RAW = os.environ.get("BIGQUERY_DATASET_RAW")

HOME_DIR = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
DOWNLOAD_DIR = os.path.join(HOME_DIR, "tmp_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
EXTRACT_DIR = os.path.join(DOWNLOAD_DIR, "extracted_files")
os.makedirs(EXTRACT_DIR, exist_ok=True)
ZIP_FILE_URL = os.environ.get("ZIP_FILE_URL")


# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "start_date": pendulum.today("UTC").add(days=-1),
    "catchup": False,
    "schedule": pendulum.duration(days=1),
}


@dag(
    default_args=default_args,
    max_active_runs=1,
)
def data_ingestion_gcs_bigquery():
    @task
    def download_zip():
        zip_file_path = os.path.join(DOWNLOAD_DIR, "downloaded_file.zip")
        response = requests.get(ZIP_FILE_URL, stream=True)
        if response.status_code == 200:
            with open(zip_file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"ZIP file downloaded to {zip_file_path}")
            return zip_file_path
        else:
            raise Exception(
                f"Failed to download file. Status code: {response.status_code}"
            )

    @task
    def extract_zip(zip_file_path):
        print(f"Extracting zip file: {zip_file_path}")
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            print("using extractall now")
            zip_ref.extractall(EXTRACT_DIR)
            print(f"ZIP file extracted to {EXTRACT_DIR}")
        return EXTRACT_DIR

    file_location = extract_zip(download_zip())

    upload_to_gcs_task = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src=f"{EXTRACT_DIR}/*.csv",  # Assuming extracted files are CSV
        dst="data/",  # Specify the destination prefix inside the GCS bucket
        bucket=GCP_GCS_DATA_BUCKET,
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

    gcs_files = list_gcs_files(bucket_name=GCP_GCS_DATA_BUCKET)

    # example from https://github.com/astronomer/webinar-task-groups/blob/main/dags/task_group_mapping_use_case.py
    @task_group(group_id="get_table_name_and_load_to_bq")
    def get_table_name_and_load_to_bq(file_name):
        @task
        def generate_table_name(file_name: str) -> str:
            """Generates sanitized BigQuery table names from GCS file names."""
            table_name = re.sub(
                r"[^a-zA-Z0-9_]", "_", file_name.split("/")[-1].replace(".csv", "")
            )
            final_table_names = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET_RAW}.{table_name}"
            return final_table_names

        table_name = generate_table_name(file_name)

        load_to_bq = GCSToBigQueryOperator(
            task_id="load_csv_to_bq",
            bucket=GCP_GCS_DATA_BUCKET,
            source_format="CSV",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            autodetect=True,
            source_objects=[file_name],
            destination_project_dataset_table=table_name,
        )

        table_name >> load_to_bq

    tg_object = get_table_name_and_load_to_bq.expand(file_name=gcs_files)

    file_location >> upload_to_gcs_task >> gcs_files >> tg_object


data_ingestion_gcs_bigquery()
