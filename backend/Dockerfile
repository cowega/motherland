# ==========================================
# CТАДИЯ 1: Сборка зависимостей (Builder)
# ==========================================
FROM python:3.10-slim AS builder

# Запрет записи байткода (.pyc) и принудительный вывод логов без буферизации
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Установка системных утилит для сборки (если потребуются компиляторы для колес)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание изолированного виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ==========================================
# СТАДИЯ 2: Финальный легковесный образ (Runner)
# ==========================================
FROM python:3.10-slim AS runner

# Настройка переменных окружения для работы venv и оптимизации Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

WORKDIR /app

# Установка runtime-зависимостей (например, libpq для PostgreSQL клиентов)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Скопировать установленное виртуальное окружение из builder-стадии
COPY --from=builder /opt/venv /opt/venv

# Скопировать исходный код бэкенда
COPY app/ ./app/

# Создание и переключение на безопасность: запуск от не-root пользователя
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT}

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
