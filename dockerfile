ARG IMAGE_TAG

FROM python:3.12

WORKDIR /app

# Установка FFmpeg и библиотеки Opus
RUN apt-get update && apt-get install -y ffmpeg libopus0

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

LABEL version=$IMAGE_TAG

CMD ["python", "main.py"]
