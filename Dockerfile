# Pythonイメージをベースにする
FROM python:3.8-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要ファイルをコピー
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY keep_alive.py keep_alive.py

# パッケージインストール
RUN pip install -r requirements.txt

# コンテナ起動時にBotを実行
CMD ["python", "main.py"]
