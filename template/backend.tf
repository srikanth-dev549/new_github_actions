terraform {
  backend "gcs" {
    bucket  = "gcp_terraform_iam_roles"
    prefix  = "terraform.tfstate"
  }
}
