# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY .. .

# Делаем entrypoint.sh исполняемым
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Указываем ENTRYPOINT
ENTRYPOINT ["/entrypoint.sh"]

# Команда запуска uvicorn-сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
