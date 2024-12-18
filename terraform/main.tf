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