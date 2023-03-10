terraform {
  backend "gcs" {
    bucket  = "gcp_terraform_iam_roles"
    prefix  = "$PROJECT_NAME-state-file/terraform.tfstate"
  }
}
