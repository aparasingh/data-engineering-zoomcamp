terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.45.0"
    }
  }
}

provider "google" {
  # Configuration options
  project     = "terraform-learn-467211"
  region      = "europe-west2"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-learn-467211-terra-bucket"
  location      = "EUROPE-WEST2"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}