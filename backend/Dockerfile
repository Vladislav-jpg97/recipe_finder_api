# Базовый образ
FROM python:3.12-slim

# ENV переменные (добавляем путь для пользовательских скриптов Python)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Рабочая директория
WORKDIR /app

# Создание непривилегированного пользователя appuser заранее
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app

# Переходим на пользователя до установки зависимостей, чтобы ставить их в его локальное окружение
USER appuser

# Копирование и установка зависимостей с флагом --user
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Копирование исходного кода и конфигураций с правами пользователя
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser alembic.ini ./
COPY --chown=appuser:appuser migrations/ ./migrations/

# Открытие порта
EXPOSE 8000

# Healthcheck на /health эндпоинт
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

CMD ["python", "-m", "uvicorn", "backend.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]