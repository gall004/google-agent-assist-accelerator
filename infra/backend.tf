# Remote state configuration
# Create the GCS bucket before initializing:
#   gsutil mb gs://${GCP_PROJECT_ID}-tfstate
#   gsutil versioning set on gs://${GCP_PROJECT_ID}-tfstate

terraform {
  backend "gcs" {
    bucket = "YOUR_PROJECT_ID-tfstate"
    prefix = "aa-accelerator"
  }
}
