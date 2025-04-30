variable "project_id" {
  description = "Google Cloud プロジェクト ID"
  type        = string
}

variable "location" {
  description = "Google Cloud リージョン"
  type        = string
}

variable "app_name" {
  description = "アプリケーション名"
  type        = string
}

variable "artifact_registry_repo_name" {
  description = "Artifact Registry リポジトリ名"
  type        = string
}

variable "artifact_registry_image_name" {
  description = "Artifact Registry イメージ名"
  type        = string
}
