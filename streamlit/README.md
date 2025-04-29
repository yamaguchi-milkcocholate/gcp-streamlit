# 開発手順

- ローカルでの streamlit の開発

```shell
uv run streamlit run home.py --server.enableCORS=false --server.port=8501
```

- Dockerfile から参照する依存関係を更新

```shell
uv pip freeze > requirements.txt
```
