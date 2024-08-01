# Используем официальный образ Python
FROM python3.12

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в рабочую директорию

COPY . .

# Указываем команду для запуска бота

CMD ["python", "main.py"]