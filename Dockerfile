FROM python:3.9-slim

# アプリケーションのソースコードをコピーするディレクトリを変更
WORKDIR /app

# requirements.txtとソースコードをコピー
# 以前のCOPYコマンドはパスが間違っていたため修正します
COPY ./src /app
COPY ./requirements.txt /app

# 必要なPythonパッケージをインストール
RUN pip install -r requirements.txt

# 環境変数PORTの値を受け取り、デフォルトとして8080を使用
ENV PORT=8080

# Gunicornでアプリケーションを実行
# Flaskアプリケーションがsetup.py内で定義されているため、
# アプリケーションのインポートパスを適切に設定する必要があります。
# ここでの "app:app" は例としています。実際のアプリケーションのモジュールと変数名に合わせて変更してください。
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app.setup:app"]
