module "artifact_registry" {
  source  = "GoogleCloudPlatform/artifact-registry/google"
  version = "~> 0.3"

  project_id    = "my-playground-458212"
  location      = "asia-northeast1"
  format        = "DOCKER"
  repository_id = "gcp-streamlit-docker-repo"
}
