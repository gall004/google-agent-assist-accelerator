# Google Agent Assist Accelerator — Terraform
# This file defines the GCP infrastructure resources.
# Actual resource definitions will be added in Phase 2+.

terraform {
  required_version = ">= 1.7"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
