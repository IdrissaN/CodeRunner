resource "google_storage_bucket_object" "get_group_activities" {
    name = "dags/get_group_activities.py"
    content = templatefile("${path.module}/dags/get_group_activities.py", {
        region = var.region
        zone = var.zone
        datastore_bucket = var.datastore_bucket
        project_id = var.project_id
    })
    bucket = var.composer_bucket
}

resource "google_storage_bucket_object" "coderunner_dag" {
    name = "dags/coderunner_dag.py"
    source = "${path.module}/dags/coderunner_dag.py"
    bucket = var.composer_bucket
}

resource "google_storage_bucket_object" "config" {
    name = "dags/config.py"
    source = "${path.module}/dags/config.py"
    bucket = var.composer_bucket
}

resource "google_storage_bucket_object" "strava_tokens" {
    name = "dags/strava_tokens.json"
    source = "${path.module}/dags/strava_tokens.json"
    bucket = var.composer_bucket
}