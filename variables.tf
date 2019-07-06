variable "credentials_file_path" {
  type = "string"
  description = "Location of the gcp credentials."
  default     = "C:\\Users\\andyl\\.ssh\\serverless-siem-47ef95c35c20.json"
}

variable "region" {
  type = "string"
  default = "us-central1"
}

variable "project_id" {
 type= "string"
 default = "serverless-siem"
}

variable "topic_name" {
  type = "string"
  default = "event-stream"
}