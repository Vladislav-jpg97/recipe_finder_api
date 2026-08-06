# Урок 11 — Домашняя работа

## Recipe Finder API — Docker Compose

---

## Контекст

Продолжаем **Recipe Finder API**. В уроке 10 приложение было упаковано в Docker контейнер, но PostgreSQL и Redis запускались отдельно. Сейчас переводим весь стек на Docker Compose.

После выполнения: `docker compose up --build -d` запускает PostgreSQL, Redis, миграции и Recipe Finder API одной командой.

---

## Часть 1 — docker-compose.yml

Создай `docker-compose.yml` в корне проекта Recipe Finder. Файл должен содержать четыре сервиса:

### Сервис postgres

| Поле | Значение |
| --- | --- |
| `image` | `postgres:16-alpine` |
| `container_name` | `recipe_postgres` |
| Переменные окружения | Брать из `.env.docker` через `${ПЕРЕМЕННАЯ}` |
| Volume | Named volume `recipe_postgres_data` монтировать в `/var/lib/postgresql/data` |
| Порт | `5432:5432` (для доступа через DBeaver) |
| `restart` | `unless-stopped` |
| `healthcheck` | `pg_isready` с интервалом 10s, таймаутом 5s, 5 попытками |

### Сервис redis

| Поле | Значение |
| --- | --- |
| `image` | `redis:7-alpine` |
| `container_name` | `recipe_redis` |
| `command` | Включить AOF persistence |
| Volume | Named volume `recipe_redis_data` монтировать в `/data` |
| Порт | `6379:6379` |
| `restart` | `unless-stopped` |
| `healthcheck` | `redis-cli ping` с интервалом 10s, таймаутом 5s, 5 попытками |

### Сервис migrate

| Поле | Значение |
| --- | --- |
| `build` | Из текущей папки, stage `production` |
| `container_name` | `recipe_migrate` |
| `command` | Применить все Alembic миграции |
| `env_file` | `.env.docker` |
| `depends_on` | `postgres` должен быть `healthy` |
| `restart` | Не перезапускать после завершения |

### Сервис web

| Поле | Значение |
| --- | --- |
| `build` | Из текущей папки, stage `production` |
| `container_name` | `recipe_web` |
| `env_file` | `.env.docker` |
| Порт | `8000:8000` |
| `depends_on` | `postgres: healthy`, `redis: healthy`, `migrate: completed_successfully` |
| `restart` | `unless-stopped` |
| `healthcheck` | `GET /health`, интервал 30s, таймаут 10s, 3 попытки, start_period 15s |

В конце файла объяви два named volumes: `recipe_postgres_data` и `recipe_redis_data`.

---

## Часть 2 — .env.docker

Создай `.env.docker` с переменными для Docker Compose.

Обязательные переменные:

| Переменная | Что должно отличаться от .env |
| --- | --- |
| `DATABASE_URL` | Хост — имя сервиса `postgres`, не `localhost` |
| `DB_USER` | Имя пользователя PostgreSQL |
| `DB_PASSWORD` | Пароль PostgreSQL |
| `DB_NAME` | Имя базы данных |
| `REDIS_URL` | Хост — имя сервиса `redis`, не `localhost` |
| `SECRET_KEY` | Любая строка для разработки |
| `DEBUG` | `False` |

Обязательно добавь `.env.docker` в `.gitignore`.

Создай `.env.docker.example` с теми же ключами, но без значений — закоммить его в git.

---

## Часть 3 — Makefile

Добавь команды в `Makefile`:

| Команда | Что делает |
| --- | --- |
| `make up` | Запустить стек в фоне с пересборкой образов |
| `make down` | Остановить и удалить контейнеры (volumes не трогать) |
| `make reset` | `down` + удалить все volumes (сброс данных) |
| `make logs` | Логи сервиса `web` в реальном времени |
| `make migrate` | Запустить `alembic upgrade head` внутри контейнера |
| `make shell` | Открыть bash внутри контейнера `web` |
| `make psql` | Подключиться к PostgreSQL через `psql` |

---

## Часть 4 — Проверка

Последовательно выполни:

```bash
make up
```

Убедись что:

- `docker compose ps` показывает все сервисы как `running` (migrate — `exited 0`)
- `curl http://localhost:8000/health` возвращает `{"status": "ok"}`
- `curl http://localhost:8000/docs` открывается Swagger UI
- Создай рецепт через API и убедись что он сохраняется в БД

Выполни:

```bash
make down
make up
```

Данные рецепта должны сохраниться после перезапуска (named volume работает).

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| Все 4 сервиса в Compose файле | 15 |
| `healthcheck` у postgres и redis | 15 |
| `migrate` с `restart: "no"` и `condition: service_healthy` | 15 |
| `web` ждёт `migrate: service_completed_successfully` | 15 |
| `.env.docker` с именами сервисов вместо localhost | 15 |
| Named volumes и данные сохраняются после `down/up` | 10 |
| Makefile с командами `up`, `down`, `reset`, `logs` | 15 |

---

## Что проверит преподаватель

```bash
# Чистый запуск
docker compose down -v
make up

# Все сервисы запущены
docker compose ps

# API работает
curl http://localhost:8000/health

# Данные сохраняются
# (создать рецепт, сделать down, up, проверить что рецепт есть)

# migrate не перезапускается
docker compose ps migrate
# Status: Exited (0)
```
