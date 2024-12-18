terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.14.0"
    }
  }
  backend "gcs" {
    bucket = "onyx-descent-417702-terra-bucket"
    prefix  = "terraform/state"
  }
}