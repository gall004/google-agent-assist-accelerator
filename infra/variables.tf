variable "gcp_project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "gcp_region" {
  description = "The GCP region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "ui_connector_docker_image" {
  description = "Docker image URI for the UI Connector service"
  type        = string
  default     = ""
}

variable "cloud_pubsub_interceptor_docker_image" {
  description = "Docker image URI for the Cloud Pub/Sub Interceptor service"
  type        = string
  default     = ""
}

variable "redis_tier" {
  description = "Memorystore Redis tier"
  type        = string
  default     = "BASIC"
}

variable "redis_memory_size_gb" {
  description = "Memorystore Redis memory size in GB"
  type        = number
  default     = 1
}
