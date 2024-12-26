provider "google" {
  project = var.project_id
  region  = var.project_region
}

resource "google_storage_bucket" "default" {
  name     = var.tf_backend_gcs_bucket_name
  location = var.project_location

  force_destroy               = false
  public_access_prevention    = "enforced"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}

resource "google_storage_bucket" "data-storage-bucket" {
  name                        = var.data_gcs_bucket_name
  location                    = var.project_location
  force_destroy               = true
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_service_account" "nba-pipeline-sa" {
  account_id   = "nba-pipeline-sa"
  display_name = "nba-pipeline service account"
  description  = "SA for nba pipeline project"
}

# https://stackoverflow.com/questions/61661116/want-to-assign-multiple-google-cloud-iam-roles-to-a-service-account-via-terrafor
resource "google_project_iam_member" "nba-pipeline-sa-roles" {
  project = var.project_id
  for_each = toset([
    "roles/viewer",
    "roles/bigquery.admin",
    "roles/storage.admin",
  ])
  role   = each.key
  member = "serviceAccount:${google_service_account.nba-pipeline-sa.email}"
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = "nba_pipeline_dataset"
  project    = var.project_id
  location   = var.project_region
}

resource "google_bigquery_dataset" "nba_pipeline_dataset_curated" {
  dataset_id = "nba_pipeline_dataset_curated"
  project    = var.project_id
  location   = var.project_region
}
