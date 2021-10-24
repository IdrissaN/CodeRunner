provider "google" {
    region = var.region
    project = var.project_id
    #credentials = var.tfs_service_account
}

module "composer-module" {
    source = "./composer-module"
    region = var.region
    zone = var.zone
    project_id = var.project_id
    datastore_bucket = var.datastore_bucket
    composer_bucket = var.composer_bucket
    schedule_interval = var.schedule_interval
    tfs_service_account = var.tfs_service_account
}

output "path" {
    value = path.module
}