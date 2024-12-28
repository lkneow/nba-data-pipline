resource "google_bigquery_dataset" "nba_pipeline_dataset_raw" {
  dataset_id = "nba_pipeline_dataset_raw"
  project    = var.project_id
  location   = var.project_region
}

resource "google_bigquery_dataset" "nba_pipeline_dataset_curated" {
  dataset_id = "nba_pipeline_dataset_curated"
  project    = var.project_id
  location   = var.project_region
}
