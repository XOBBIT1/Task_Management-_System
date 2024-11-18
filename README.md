# Task_Management-_System
A web-based task management application that allows users to create, edit, delete, and track the status of tasks.


Этот проект состоит из FastAPI сервера для backend и Next.js клиента для frontend. Инструкция ниже поможет вам развернуть сервер, клиент и базу данных с помощью Docker.

## Требования

- Python 3.12+
- Docker и Docker Compose
- Node.js 22.11.0+ (для локальной разработки фронтенда, если требуется)

## Шаги для запуска проекта

### 1. Запуск базы данных через Docker Compose

В корне проекта (там, где находится `docker-compose.yml`), выполните команду:

```bash
docker-compose up -d
```
Это запустит базу данных в docker-compose.yml.


### 2. Запуск FastAPI сервера
Перейдите в директорию app и запустите FastAPI сервер:

Установите зависимости:

```bash
pipenv install
pipenv shell 

или 

pip install -r requirements.txt -> если дейлаеете своё виртуальное окружение 
```

```bash
uvicorn app.main:app --reload
```

FastAPI сервер запустится по умолчанию на http://127.0.0.1:8000.

### 3. Запуск Next.js клиента
Перейдите в директорию Next.js приложения:

```bash
cd app/frontend/task_management_system
```

Установите зависимости:

```bash
npm install
```
Затем запустите приложение в режиме разработки:

```bash
npm run dev
```