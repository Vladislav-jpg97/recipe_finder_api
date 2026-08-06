# Урок 3 — Домашняя работа

## Recipe Finder API — База данных

---

## Контекст

Продолжаем **Recipe Finder API**. До этого рецепты хранились как список словарей в памяти — они терялись при перезапуске. Сейчас подключаем PostgreSQL: создаём SQLAlchemy модель, настраиваем Alembic и переписываем эндпоинты на реальные запросы к БД.

---

## Часть 1 — Зависимости и конфигурация

Добавь в проект нужные пакеты:

```bash
poetry add sqlalchemy asyncpg alembic
```

Обнови `.env` — добавь строку подключения к БД:

```text
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/recipe_finder
```

Обнови `app/config.py` — добавь поле `database_url: str` (без дефолта, оно обязательно).

---

## Часть 2 — SQLAlchemy модель

Создай `app/models.py` с моделью `Recipe`.

Используй SQLAlchemy 2.0 стиль: `DeclarativeBase`, `Mapped`, `mapped_column` — как делали в DevTalks на уроке.

Поля модели:

| Поле | Тип Python | Особенности |
| --- | --- | --- |
| `id` | `int` | primary key |
| `title` | `str` | max 200 символов |
| `slug` | `str` | max 220, unique, indexed |
| `cuisine` | `str` | max 50, indexed |
| `difficulty` | `str` | max 10 |
| `cooking_time` | `int` | — |
| `servings` | `int` | — |
| `calories_per_serving` | `int` | — |
| `ingredients` | `str` | Text, хранить как JSON строку |
| `is_vegetarian` | `bool` | default False |
| `rating` | `float` | default 0.0 |
| `created_at` | `datetime` | server_default=func.now() |

Поле `ingredients` хранит список ингредиентов как JSON строку. При сохранении используй `json.dumps(список)`, при чтении — `json.loads(строка)`.

---

## Часть 3 — Подключение к БД

Создай `app/database.py` по образцу из урока DevTalks:

- `create_async_engine` с URL из `settings`
- `async_sessionmaker` с `expire_on_commit=False`
- функция-зависимость `get_db` с `yield` и rollback при исключении

---

## Часть 4 — Alembic

Инициализируй Alembic:

```bash
alembic init migrations
```

Настрой `migrations/env.py`:

- URL берётся из `settings.database_url` (не из `alembic.ini`)
- `target_metadata` указывает на `Base.metadata` из твоих моделей
- Используй async engine (паттерн из материала урока)

Создай и примени первую миграцию:

```bash
alembic revision --autogenerate -m "create recipes table"
alembic upgrade head
```

---

## Часть 5 — Переписываем эндпоинты

Удали список `RECIPES` из памяти. Каждый эндпоинт теперь получает `db: AsyncSession = Depends(get_db)` и работает с БД.

Перепиши следующие эндпоинты:

### POST /api/v1/recipes/

Создаёт новый рецепт в БД. Список ингредиентов сериализуй в JSON строку при сохранении. После `commit` вызови `refresh` чтобы получить сгенерированные БД значения (`id`, `created_at`). Возвращает `RecipeDetail`.

### GET /api/v1/recipes/{slug}

Делает `SELECT` по `slug`. Если не найдено — 404.

### GET /api/v1/recipes/

Делает `SELECT` с фильтрами через `WHERE`. Фильтрация по `cuisine` и `is_vegetarian` должна происходить в SQL, не в Python.

### PATCH /api/v1/recipes/{slug}

Находит рецепт, обновляет поля, делает `commit`. Если не найдено — 404.

---

## Часть 6 — Начальные данные

Создай скрипт `seed.py` в корне проекта. Скрипт при запуске добавляет в БД рецепты из урока 1 (минимум 8 штук).

Запускать через:

```bash
poetry run python seed.py
```

Требования к скрипту:

- использует `asyncio.run` — скрипт асинхронный
- создаёт свой engine и сессию (не импортирует `get_db`)
- не добавляет дубликаты при повторном запуске (проверяй по `slug`)
- выводит сколько рецептов добавлено

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| Модель `Recipe` + миграция применена | 20 |
| `POST` сохраняет рецепт в БД | 20 |
| `GET /{slug}` читает из БД, 404 при отсутствии | 15 |
| `GET /` фильтрует через SQL | 20 |
| `PATCH` обновляет запись в БД | 15 |
| `seed.py` работает, не дублирует записи | 10 |

---

## Что проверит преподаватель

- `alembic upgrade head` проходит без ошибок
- `POST /api/v1/recipes/` создаёт запись, она появляется в `GET /`
- Перезапуск `uvicorn` — данные не теряются
- `GET /api/v1/recipes/?cuisine=italian` выполняет `WHERE cuisine = 'italian'` (проверь через `echo=True` в engine)
- `GET /api/v1/recipes/несуществующий` возвращает 404
- Повторный запуск `seed.py` не создаёт дубликаты
