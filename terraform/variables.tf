variable "project_id" {
  description = "GCP Project"
}

variable "project_region" {
  description = "region for GCP Project"
  default     = "asia-southeast-1"
}

variable "project_location" {
  description = "ASIA"
  default     = "ASIA"
}

variable "tf_backend_gcs_bucket_name" {
  description = "tf backend GCS Bucket name"
}

variable "data_gcs_bucket_name" {
  description = "data GCS Bucket name"
}

variable "dbt_docs_bucket_name" {
  description = "dbt docs GCS Bucket name"
}
