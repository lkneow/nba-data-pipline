import os

from airflow.utils.dates import days_ago
from cosmos import (
    DbtDag,
    DbtTaskGroup,
    ExecutionConfig,
    ProfileConfig,
    ProjectConfig,
    RenderConfig,
)
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping
from cosmos.constants import TestBehavior

GCP_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
GCS_BUCKET = os.environ.get("GCP_GCS_BUCKET")
BIGQUERY_DATASET_CURATED = os.environ.get("BIGQUERY_DATASET_CURATED")

HOME_DIR = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

# The path to the dbt project
DBT_PROJECT_PATH = f"{HOME_DIR}/dags/nba_data_pipeline"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = f"{HOME_DIR}/dbt_venv/bin/dbt"

profile_config = ProfileConfig(
    profile_name="nba_data_pipeline",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
        conn_id = 'gcp_conn',
        profile_args = {
            'project': GCP_PROJECT_ID,
            'dataset': BIGQUERY_DATASET_CURATED,
            'keyfile': '/.google/credentials/google_credentials.json',
            'location': 'asia-southeast1',
            'job_retries': 1,
            'job_execution_timeout_seconds': 300,
            'method': 'service-account'
        },
    )
)

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)

render_config = RenderConfig(
    emit_datasets=False,
    test_behavior=TestBehavior.AFTER_EACH
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'start_date': days_ago(1),  # Replace with your start date
    'catchup': False,
    'schedule_interval': '@daily'
}

simple_dag = DbtDag(
    # dbt/cosmos-specific parameters
    project_config=ProjectConfig(DBT_PROJECT_PATH),
    profile_config=profile_config,
    execution_config=execution_config,
    # normal dag parameters
    default_args=default_args,
    dag_id="simple_dag"
)