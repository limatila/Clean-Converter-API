FROM python:3.11

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y git

WORKDIR /app

RUN git clone https://github.com/limatila/clean-converter-api /app

RUN pip install --no-cache-dir -r requirements.txt
