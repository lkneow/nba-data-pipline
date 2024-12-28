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
