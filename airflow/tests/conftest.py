import pytest
from airflow.models import DagBag


@pytest.fixture
def mock_env_vars(mocker):
    """Fixture to mock environment variables."""
    mocker.patch.dict(
        "os.environ",
        {
            "GCP_PROJECT_ID": "test_project",
            "GCP_GCS_DATA_BUCKET": "test_bucket",
            "BIGQUERY_DATASET_RAW": "test_dataset",
            "ZIP_FILE_URL": "http://example.com/test.zip",
            "AIRFLOW_HOME": "/tmp/airflow_test",
            "DOWNLOAD_DIR": "/tmp/airflow_test/tmp_downloads",
            "EXTRACT_DIR": "/tmp/airflow_test/tmp_downloads/extracted_files",
        },
    )


@pytest.fixture()
def dagbag():
    return DagBag(include_examples=False)
