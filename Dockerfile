# Python の公式イメージをベースイメージとして使用
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gnupg \
    unixodbc \
    unixodbc-dev \
    g++ \
    curl \
    apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定する
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=8000

# 依存関係のあるファイルを作業ディレクトリにコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ローカルの src ディレクトリの内容を作業ディレクトリにコピー
COPY src/ ./src/

# gunicorn を使ってアプリを実行するコマンドを定義
CMD gunicorn --bind 0.0.0.0:$PORT src.app.setup:app