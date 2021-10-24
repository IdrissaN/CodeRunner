variable "project_id" {
  description = "The ID of the project"
  type    = string
}

variable "region" {
  description = "The GCP region to retrieve a short name for (ex. `us-central1)."
  type        = string
}

variable "zone" {
  description = "The GCP zone"
  type        = string
}

variable "schedule_interval" {
  description = "Cron expression"
  type        = string
}

variable "datastore_bucket" {
  description = "Name of the GCS bucket used for data storage and metadata, without the gs:// prefix"
  type        = string
}

variable "composer_bucket" {
  description = "Name of the GCS bucket used for storing python files, without the gs:// prefix"
  type        = string
}

variable "tfs_service_account" {
  description = "Service account used to deploy the terraform code"
  type        = string
}