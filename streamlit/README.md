# 開発手順

- ローカルでの streamlit の開発

```shell
uv run streamlit run home.py --server.enableCORS=false --server.port=8501
```

- Dockerfile から参照する依存関係を更新

```shell
uv pip freeze > requirements.txt
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
