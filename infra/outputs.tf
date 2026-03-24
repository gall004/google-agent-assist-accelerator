output "ui_connector_url" {
  description = "URL of the deployed UI Connector Cloud Run service"
  value       = ""
}

output "interceptor_url" {
  description = "URL of the deployed Cloud Pub/Sub Interceptor Cloud Run service"
  value       = ""
}

output "redis_host" {
  description = "Host address of the Memorystore Redis instance"
  value       = ""
  sensitive   = true
}
