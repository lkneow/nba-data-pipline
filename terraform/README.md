# Terraform

## What I did after installation

Created a few files
- [`terraform.tf`](terraform.tf)
- [`main.tf`](main.tf)
- [`variables.tf`](variables.tf)
- `terraform.tfvars` (this is in .gitignore)
- [`bq.tf`](bq.tf)
- [`sa.tf`](sa.tf)

In order to have the terraform state to be store in gcs, we have to first create the bucket

I ran `terraform apply` without the backend portion in `terraform.tf`.

Once the bucket is created, I added the backend portion and ran `terraform init -migrate-state`

Note all this is only possible since I authenticated to gcloud with my own account, i.e. admin/owner. Will have to add the relevant permissions if using a service account

## Relevant links
- https://developer.hashicorp.com/terraform/language/backend/gcs#gcs
- https://cloud.google.com/docs/terraform/resource-management/store-state#before-you-begin
