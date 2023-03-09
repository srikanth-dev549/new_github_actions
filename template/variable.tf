variable "data_file" {
    type = string
    default = "$PROJECT_NAME-data.json"
}

variable "bucket_name" {
    type = string
    default = "$PROJECT_NAME-STATE-FILE-IAM-ROLES"
}

