# gcp-streamlit

## ローカルから Artifact Registory に Docker イメージをプッシュ

```shell
cd streamlit

# イメージをビルド
docker build -t asia-northeast1-docker.pkg.dev/my-playground-458212/gcp-streamlit-docker-repo/streamlit:latest .

# Dockerログイン
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
# Artifact Registoryにプッシュ
docker push asia-northeast1-docker.pkg.dev/my-playground-458212/gcp-streamlit-docker-repo/streamlit:latest
```

## ローカルから Cloud Run にデプロイ

```shell
gcloud run deploy managed-streamlit \
--image asia-northeast1-docker.pkg.dev/my-playground-458212/gcp-streamlit-docker-repo/streamlit:latest \
--platform managed \
--region asia-northeast1 \
--port 8501 \
--allow-unauthenticated
```

## 参考

- streamlit x gcp
  - https://future-architect.github.io/articles/20250422a/
  - https://zenn.dev/google_cloud_jp/articles/streamlit-01-hello
- gcp x github-actions
  - https://zenn.dev/cloud_ace/articles/7fe428ac4f25c8
