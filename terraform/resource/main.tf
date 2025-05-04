locals {
  project_id = "my-playground-458212"
  location   = "asia-northeast1"
}

module "artifact_registry" {
  source  = "GoogleCloudPlatform/artifact-registry/google"
  version = "~> 0.3"

  project_id    = local.project_id
  location      = local.location
  format        = "DOCKER"
  repository_id = "gcp-streamlit-docker-repo"
}

module "workload_identity" {
  source            = "../module/workload_identity"
  project_id        = local.project_id
  github_repo_owner = "yamaguchi-milkcocholate"
  github_repo_name  = "gcp-streamlit"
}

# Creating secret
resource "google_secret_manager_secret" "ar-svc-secret" {
  project   = local.project_id
  secret_id = "google-ai-studio-api-key"

  labels = {
    label = "gcp-streamlit"
  }
  replication {
    user_managed {
      replicas {
        location = local.location
      }
    }
  }
}
