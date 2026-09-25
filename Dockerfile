FROM python:3.12-slim

# Отключаем буферизацию вывода Python и запись .pyc файлов
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем системные зависимости для сборки (C-библиотеки для argon2 и asyncpg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код
COPY . .

# Запускаем FastAPI через Uvicorn на порту 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]