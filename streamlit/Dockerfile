FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# streamlitのデフォルトPORT番号
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "home.py", "--server.enableCORS=false", "--server.port=8501"]
