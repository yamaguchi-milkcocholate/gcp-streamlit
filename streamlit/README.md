# 開発手順

- ローカルでの streamlit の開発

```shell
uv run streamlit run home.py --server.enableCORS=false --server.port=8501
```

- Dockerfile から参照する依存関係を更新

```shell
uv pip freeze > requirements.txt
```

- Docker コンテナを起動
  - 基本的には uv 環境を直接使用して開発可能だが、cloud run のコンテナイメージに関係する開発をしたい場合は、ローカルで Docker コンテナを立てて streamlit を実行する

```shell
cd streamlit
# ビルド
docker compose build
# 起動
docker compose up
# streamlitにアクセス
http://localhost:8501/
```

# デプロイ

- ローカルから Terraform コマンドを実行

```shell
cd terraform/prod
terraform apply
```

# 準備

- LangGraph で Dag を描画するために必要なライブラリをインストール

```shell
brew install graphviz
```

# 参考

- langchain x GCP Vertex AI
  - https://python.langchain.com/docs/integrations/providers/google/#google-cloud
- Gemini の料金
  - https://cloud.google.com/vertex-ai/generative-ai/pricing?hl=ja
