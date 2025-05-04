FROM python:3.10-slim-bullseye

WORKDIR /app

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN apt-get update && apt-get install -y \
    libopencv-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# streamlitのデフォルトPORT番号
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "home.py", "--server.enableCORS=false", "--server.port=8501"]
