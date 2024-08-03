ARG IMAGE_TAG

FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache ffmpeg

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

LABEL version=$IMAGE_TAG

CMD ["python", "main.py"]
