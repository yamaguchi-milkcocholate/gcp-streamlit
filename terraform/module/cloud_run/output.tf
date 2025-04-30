output "url" {
  value = google_cloud_run_service.streamlit_service.status[0].url
}
