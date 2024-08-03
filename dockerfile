ARG IMAGE_TAG


# Используем официальный образ Python 3.12
FROM python:3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в рабочую директорию
COPY . .

# Указываем версию образа
LABEL version=$IMAGE_TAG

# Указываем команду для запуска бота
CMD ["python", "main.py"]

