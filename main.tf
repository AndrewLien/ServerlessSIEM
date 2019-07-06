

// Configure the Google Cloud provider
provider "google" {
  region      = "${var.region}"
  credentials = "${file("${var.credentials_file_path}")}"
  project = "${var.project_id}"
}

// Configure windows event stream topic
resource "google_pubsub_topic" "windows-eventstream" {
  name = "windows-eventstream"
  labels = {
    source = "windows"
  }
}

// Configure dataflow GCS holding location
resource "google_storage_bucket" "dataflow" {
  name     = "dataflow_artifacts"
  location = "${var.region}"
  force_destroy = true
}

// Configure sample big data job to pull in windows eventstream
resource "google_dataflow_job" "big_data_job" {
    name = "dataflow-job"
    template_gcs_path = "gs://dataflow-templates/latest/Cloud_PubSub_to_GCS_Text"
    temp_gcs_location = "gs://${google_storage_bucket.dataflow.name}/tmp_dir"
    zone =  "${var.region}-f"
    parameters = {
        inputTopic = "projects/${var.project_id}/topics/${google_pubsub_topic.windows-eventstream.name}"
        outputDirectory = "gs://${google_storage_bucket.dataflow.name}/output/"
        outputFilenamePrefix = "output-"
        outputFilenameSuffix = ".txt"
    }
    on_delete = "cancel"
}