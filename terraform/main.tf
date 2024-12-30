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

resource "google_storage_bucket" "dbt-docs-bucket" {
  name                        = var.dbt_docs_bucket_name
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
