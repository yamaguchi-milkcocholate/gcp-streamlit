resource "google_cloud_run_service" "streamlit_service" {
  name     = var.app_name
  location = var.location
  project  = var.project_id

  template {
    spec {
      containers {
        image = "${var.location}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo_name}/${var.artifact_registry_image_name}:latest"
        resources {
          limits = {
            memory = "512Mi"
            cpu    = "1"
          }
        }
        ports {
          container_port = 8501
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  location = google_cloud_run_service.streamlit_service.location
  project  = google_cloud_run_service.streamlit_service.project
  service  = google_cloud_run_service.streamlit_service.name
  role     = "roles/run.invoker"
  member   = "allUsers" # 誰でもアクセス可能にする場合。制限したい場合は適宜変更。
}
