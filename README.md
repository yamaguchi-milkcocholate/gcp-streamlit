# gcp-streamlit

## ローカルから Artifact Registory に Docker イメージをプッシュ

```shell
cd streamlit

# イメージをビルド
docker build -t asia-northeast1-docker.pkg.dev/my-playground-458212/gcp-streamlit-docker-repo/streamlit:0.1 .

# Dockerログイン
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
# Artifact Registoryにプッシュ
docker push asia-northeast1-docker.pkg.dev/my-playground-458212/gcp-streamlit-docker-repo/streamlit:0.1
```

## 参考

- https://future-architect.github.io/articles/20250422a/
- https://zenn.dev/google_cloud_jp/articles/streamlit-01-hello
