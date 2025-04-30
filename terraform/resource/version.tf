terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.26.0, < 7"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 5.26.0, < 7"
    }
  }
  required_version = ">= 0.13"
}
