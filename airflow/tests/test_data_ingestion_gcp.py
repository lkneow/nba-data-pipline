def test_data_ingestion_gcp_dag_import_errors(dagbag, mock_env_vars):
    """Test that there are no import errors in the DAGs."""
    assert len(dagbag.import_errors) == 0, f"DAG import errors: {dagbag.import_errors}"


def test_data_ingestion_gcp_dag_loaded(dagbag, mock_env_vars):
    """Test if the specific DAG is loaded and has the correct structure."""
    dag_id = "data_ingestion_gcs_bigquery"
    dag = dagbag.get_dag(dag_id)

    # Check if DAG is registered
    assert dag is not None, f"{dag_id} is not found in the DAGBag"

    # Check the number of tasks
    assert len(dag.tasks) > 0, "DAG has no tasks"

    # Validate task IDs
    expected_tasks = {
        "download_zip",
        "extract_zip",
        "upload_to_gcs",
        "list_gcs_files",
        "get_table_name_and_load_to_bq.generate_table_name",
        "get_table_name_and_load_to_bq.load_csv_to_bq",
    }
    task_ids = set(task.task_id for task in dag.tasks)
    assert (
        task_ids == expected_tasks
    ), f"Expected tasks {expected_tasks}, but got {task_ids}"


def test_data_ingestion_gcp_download_zip(mocker, mock_env_vars, dagbag):
    """Test the `download_zip` task with mocked environment variables."""
    # Load the DAG
    dag = dagbag.get_dag("data_ingestion_gcs_bigquery")
    download_zip_task = dag.get_task("download_zip")

    # Mock `requests.get`
    mock_get = mocker.patch("requests.get")
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.iter_content = lambda chunk_size: [b"data"]
    mock_get.return_value = mock_response

    # Run the task
    zip_file_path = download_zip_task.python_callable()

    # Assertions
    assert zip_file_path.endswith("downloaded_file.zip")
    mock_get.assert_called_once_with("http://example.com/test.zip", stream=True)


def test_extract_zip(mocker, mock_env_vars, dagbag):
    """Test the `extract_zip` task."""
    # Load the DAG
    dag = dagbag.get_dag("data_ingestion_gcs_bigquery")
    extract_zip_task = dag.get_task("extract_zip")

    # Mock zipfile.ZipFile and its extractall method
    mock_zipfile = mocker.patch("zipfile.ZipFile", autospec=True)

    # Mock context manager methods, magic method ref https://docs.python.org/3/library/unittest.mock.html#magic-methods
    mock_zip_instance = mock_zipfile.return_value
    mock_zip_instance.__enter__.return_value = (
        mock_zip_instance  # Returned object from `with` block
    )
    mock_extractall = mock_zip_instance.extractall

    # Simulate task logic
    zip_file_path = "/tmp/test.zip"
    result = extract_zip_task.python_callable(zip_file_path)

    # Assertions
    assert result == "/tmp/airflow_test/tmp_downloads/extracted_files"
    mock_zipfile.assert_called_once_with(
        zip_file_path, "r"
    )  # Verify the zip file was opened in read mode
    mock_extractall.assert_called_once_with(
        "/tmp/airflow_test/tmp_downloads/extracted_files"
    )  # Ensure extractall was called


class MockBlob:
    def __init__(self, name):
        self.name = name


def test_list_gcs_files(mocker, mock_env_vars, dagbag):
    """Test the `list_gcs_files` task."""
    # Load the DAG
    dag = dagbag.get_dag("data_ingestion_gcs_bigquery")
    list_gcs_files_task = dag.get_task("list_gcs_files")

    # Mock Google Cloud Storage Client
    mock_storage_client = mocker.patch("google.cloud.storage.Client")
    mock_client = mocker.Mock()
    mock_bucket = mocker.Mock()
    mock_blobs = [MockBlob(name="file1.csv"), MockBlob(name="file2.csv")]
    mock_bucket.list_blobs.return_value = mock_blobs
    mock_client.bucket.return_value = mock_bucket
    mock_storage_client.return_value = mock_client

    # Run the task logic
    files = list_gcs_files_task.python_callable("test_bucket")

    # Assertions
    assert files == ["file1.csv", "file2.csv"]
    mock_bucket.list_blobs.assert_called_once()
