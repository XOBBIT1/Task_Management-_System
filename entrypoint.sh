#!/bin/bash
set -e

# Проверка доступности базы данных перед запуском приложения
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Пример миграции для SQLAlchemy (если они требуются)
# echo "Running migrations..."
# alembic upgrade head

# Запуск uvicorn-сервера
exec "$@"
