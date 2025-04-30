resource "google_iam_workload_identity_pool" "main" {
  workload_identity_pool_id = "github"
  display_name              = "GitHub"
  description               = "GitHub Actions 用 Workload Identity Pool"
  disabled                  = false
  project                   = var.project_id
}

resource "google_iam_workload_identity_pool_provider" "main" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.main.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  display_name                       = "GitHub"
  description                        = "GitHub Actions 用 Workload Identity Poolプロバイダ"
  disabled                           = false
  attribute_condition                = "assertion.repository_owner == \"${var.github_repo_owner}\""
  attribute_mapping = {
    "google.subject" = "assertion.repository"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
  project = var.project_id
}

resource "google_service_account_iam_member" "workload_identity_sa_iam" {
  service_account_id = google_service_account.main.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principal://iam.googleapis.com/${google_iam_workload_identity_pool.main.name}/subject/${var.github_repo_owner}/${var.github_repo_name}"
}

resource "google_service_account" "main" {
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions Service Account"
  description  = "GitHub Actions 用 Service Account"
  project      = var.project_id
}

resource "google_project_iam_member" "artifact_registry_access" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:github-actions-sa@${var.project_id}.iam.gserviceaccount.com"
}
