locals {
  project_id = "my-playground-458212"
  location   = "asia-northeast1"
}
module "cloud_run" {
  source                       = "../module/cloud_run"
  project_id                   = local.project_id
  location                     = local.location
  app_name                     = "managed-streamlit"
  artifact_registry_repo_name  = "gcp-streamlit-docker-repo"
  artifact_registry_image_name = "streamlit"
}
