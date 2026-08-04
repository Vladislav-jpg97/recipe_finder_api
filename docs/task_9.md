# Урок 10 — Домашняя работа

## Recipe Finder API — Docker контейнер

---

## Контекст

Продолжаем **Recipe Finder API**. Упаковываем приложение в Docker контейнер. После выполнения Recipe Finder API запускается в контейнере и доступен по `http://localhost:8000/docs`.

---

## Часть 1 — .dockerignore

Создай `.dockerignore` в корне проекта.

Что нужно исключить:

| Что исключить | Причина |
| --- | --- |
| `venv/`, `.venv/` | Не нужен в образе |
| `__pycache__/`, `*.pyc` | Артефакты Python |
| `.env`, `.env.*` | Секреты не должны попасть в образ |
| `.git/` | История git не нужна |
| `tests/` | Не нужны в production образе |
| `htmlcov/`, `.coverage`, `.pytest_cache/` | Тестовые артефакты |
| `*.md` | Документация |
| `migrations/versions/` | Версии Alembic (применяются отдельно) |

Исключение: `.env.example` оставляем — это шаблон без реальных секретов.

---

## Часть 2 — requirements.txt

Установи плагин и сгенерируй `requirements.txt`:

```bash
poetry self add poetry-plugin-export
poetry export --without dev --without-hashes -f requirements.txt -o requirements.txt
```

Убедись что `requirements.txt` не находится в `.dockerignore` — он нужен для `docker build`.

---

## Часть 3 — Dockerfile

Создай `Dockerfile` в корне проекта. Требования:

**Базовый образ:** `python:3.12-slim`

**ENV переменные:**

| Переменная | Значение |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE` | `1` |
| `PYTHONUNBUFFERED` | `1` |
| `PIP_NO_CACHE_DIR` | `1` |
| `PIP_DISABLE_PIP_VERSION_CHECK` | `1` |

**Рабочая директория:** `/app`

**Порядок слоёв (от стабильного к изменяемому):**

1. Базовый образ с ENV
2. Копирование `requirements.txt`
3. `pip install -r requirements.txt`
4. Копирование `app/`, `alembic.ini`, `migrations/`
5. Создание непривилегированного пользователя `appuser`
6. `EXPOSE 8000`
7. `HEALTHCHECK` на `/health` эндпоинт
8. `CMD` с uvicorn

**CMD:** `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2`

---

## Часть 4 — Эндпоинт /health

Добавь в `app/main.py` эндпоинт для HEALTHCHECK:

- URL: `GET /health`
- Возвращает: `{"status": "ok"}`
- Статус: 200

Это единственный эндпоинт который должен работать без БД.

---

## Часть 5 — Сборка и запуск

Собери образ:

```bash
docker build -t recipe-api:latest .
```

Создай `.env.docker` (отдельный файл, не `.env`):

| Переменная | Значение |
| --- | --- |
| `DATABASE_URL` | С `host.docker.internal` вместо `localhost` |
| `REDIS_URL` | С `host.docker.internal` вместо `localhost` |
| `SECRET_KEY` | Любая строка для разработки |

Запусти контейнер:

```bash
docker run -d \
  --name recipe-api \
  -p 8000:8000 \
  --env-file .env.docker \
  recipe-api:latest
```

Убедись что `http://localhost:8000/docs` открывается.

---

## Часть 6 — Makefile

Создай `Makefile` с командами:

| Команда | Что делает |
| --- | --- |
| `make export` | `poetry export ...` → `requirements.txt` |
| `make build` | Вызывает `export`, затем `docker build` |
| `make run` | `docker run` с нужными флагами |
| `make stop` | `docker stop recipe-api && docker rm recipe-api` |
| `make logs` | `docker logs -f recipe-api` |
| `make shell` | `docker exec -it recipe-api bash` |

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| `.dockerignore` исключает `.env` и `venv/` | 10 |
| Dockerfile: зависимости копируются ДО кода | 20 |
| `PYTHONUNBUFFERED=1` и `PIP_NO_CACHE_DIR=1` в ENV | 10 |
| Непривилегированный пользователь `appuser` | 15 |
| `GET /health` работает и возвращает 200 | 10 |
| Образ собирается без ошибок | 15 |
| Контейнер запускается и `/docs` открывается | 10 |
| `Makefile` с `build`, `run`, `stop`, `logs` | 10 |

---

## Что проверит преподаватель

```bash
docker build -t recipe-api:latest .   # без ошибок

docker images recipe-api              # размер < 500 MB

docker run -d -p 8000:8000 --env-file .env.docker recipe-api:latest

docker logs recipe-api                # uvicorn startup без ошибок

curl http://localhost:8000/health     # {"status": "ok"}

docker exec recipe-api env | grep SECRET_KEY
# должен вернуть значение (есть в окружении)

docker exec recipe-api env | grep DATABASE_URL
# должен содержать host.docker.internal, не localhost

docker inspect recipe-api --format='{{.Config.User}}'
# appuser
```
