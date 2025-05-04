locals {
  project_id = "my-playground-458212"
  location   = "asia-northeast1"
}

data "google_secret_manager_secret_version" "api_key_secret" {
  project = local.project_id
  secret  = "google-ai-studio-api-key"
  version = "latest"
}

module "cloud_run" {
  source                       = "../module/cloud_run"
  project_id                   = local.project_id
  location                     = local.location
  app_name                     = "managed-streamlit"
  artifact_registry_repo_name  = "gcp-streamlit-docker-repo"
  artifact_registry_image_name = "streamlit"
  google_ai_studio_api_key     = data.google_secret_manager_secret_version.api_key_secret.secret_data
}
