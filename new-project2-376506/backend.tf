terraform {
  backend "gcs" {
    bucket  = "gcp_terraform_iam_roles"
    prefix  = "new-project2-376506-state-file/terraform.tfstate"
  }
}
