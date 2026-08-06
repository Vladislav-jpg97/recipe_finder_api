# Урок 4 — Домашняя работа

## Recipe Finder API — Репозитории и категории

---

## Контекст

Продолжаем **Recipe Finder API**. В уроках 1–3 ты создал FastAPI приложение с Pydantic схемами, SQLAlchemy моделью и Alembic миграцией. Эндпоинты работали напрямую с `AsyncSession`.

В этом задании ты вводишь архитектурные слои как на уроке: Repository для SQL-запросов и Service для бизнес-логики. Плюс добавляешь модель `Cuisine` — отдельная таблица вместо строки `cuisine` в `Recipe`.

---

## Часть 1 — Модель Cuisine

Создай `app/models/cuisine.py` с моделью кухни. Поля:

| Поле | Тип Python | Ограничения |
| --- | --- | --- |
| `id` | `int` | primary key |
| `name` | `str` | max 100, unique |
| `slug` | `str` | max 110, unique, indexed |
| `country_code` | `str` или `None` | max 3, например "IT", "JP" |

Обнови модель `Recipe`:

- Удали поле `cuisine: str`
- Добавь `cuisine_id: int` — ForeignKey на `cuisines.id`
- При удалении кухни посты не удаляются — выбери правильное поведение

Создай и примени Alembic миграцию.

---

## Часть 2 — RecipeRepository

Создай `app/repositories/recipe_repo.py` с классом `RecipeRepository`. Класс принимает `db: AsyncSession` в конструктор.

Методы репозитория:

| Метод | Описание |
| --- | --- |
| `get_all` | SELECT всех рецептов с загруженной связью `cuisine` |
| `get_by_id` | SELECT по id, с `cuisine` |
| `get_by_slug` | SELECT по slug (без загрузки связей) |
| `add` | Добавить рецепт в сессию: `flush + refresh` |
| `delete` | Удалить рецепт из сессии: `delete + flush` |

---

## Часть 3 — CuisineRepository

Создай `app/repositories/cuisine_repo.py` с классом `CuisineRepository`. Методы:

| Метод | Описание |
| --- | --- |
| `get_all` | SELECT всех кухонь, отсортировать по name |
| `get_by_id` | SELECT по id |
| `get_by_slug` | SELECT по slug |
| `add` | flush + refresh |
| `delete` | delete + flush |

---

## Часть 4 — CuisineService

Создай `app/services/cuisine_service.py` с классом `CuisineService`. Конструктор принимает `repo: CuisineRepository` и `db: AsyncSession`.

Поведение методов:

### get_all

Возвращает все кухни.

### get_or_404

Принимает `cuisine_id: int`. Если кухня не найдена — поднимает 404.

### create

Принимает `name` и `country_code`. Генерирует `slug` из `name`. Если slug уже занят — 409 Conflict. Коммитит после успешного добавления.

### delete

Принимает `cuisine_id`. Удаляет кухню. Коммитит.

---

## Часть 5 — RecipeService

Создай `app/services/recipe_service.py` с классом `RecipeService`. Конструктор принимает `repo: RecipeRepository` и `db: AsyncSession`.

Поведение методов:

### get_all

Возвращает все рецепты.

### get_or_404

Если рецепт не найден — 404.

### create

- Генерирует уникальный `slug` из `title`
- Если slug уже занят — добавляет числовой суффикс (как на уроке)
- Поле `ingredients` сериализуй через `json.dumps` перед сохранением
- Коммитит, затем возвращает рецепт с загруженной кухней

### update

- Принимает `recipe_id` и данные для обновления
- Обновляет только переданные поля (`exclude_unset=True`)
- Если изменился `title` — пересчитай slug
- Коммитит

### delete

Удаляет рецепт. Коммитит.

---

## Часть 6 — Роутеры и DI

Создай два файла роутеров:

### app/api/v1/cuisines.py

Эндпоинты:

| Метод | URL | Статус | Описание |
| --- | --- | --- | --- |
| GET | `/cuisines/` | 200 | Список всех кухонь |
| GET | `/cuisines/{cuisine_id}` | 200 | Одна кухня |
| POST | `/cuisines/` | 201 | Создать кухню |
| DELETE | `/cuisines/{cuisine_id}` | 204 | Удалить кухню |

### app/api/v1/recipes.py

Эндпоинты как в уроке 3, но через `RecipeService`:

| Метод | URL | Статус | Описание |
| --- | --- | --- | --- |
| GET | `/recipes/` | 200 | Список рецептов (фильтр `cuisine_id` query-param) |
| GET | `/recipes/{recipe_id}` | 200 | Один рецепт |
| POST | `/recipes/` | 201 | Создать рецепт |
| PATCH | `/recipes/{recipe_id}` | 200 | Обновить рецепт |
| DELETE | `/recipes/{recipe_id}` | 204 | Удалить рецепт |

В каждом роутере создай функцию-фабрику `get_XXX_service(db: AsyncSession = Depends(get_db))` которая создаёт репозиторий и сервис.

---

## Структура файлов

```text
app/
├── api/v1/
│   ├── cuisines.py
│   └── recipes.py
├── models/
│   ├── cuisine.py
│   └── recipe.py        (обновлён)
├── repositories/
│   ├── cuisine_repo.py
│   └── recipe_repo.py
└── services/
    ├── cuisine_service.py
    └── recipe_service.py
```

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| Модель `Cuisine` + миграция применена | 15 |
| `RecipeRepository` с `selectinload` для кухни | 15 |
| `CuisineService` с проверкой уникального slug + 409 | 15 |
| `RecipeService.create` генерирует уникальный slug | 20 |
| `RecipeService.update` обновляет только переданные поля | 15 |
| DI через `Depends` в обоих роутерах | 10 |
| `DELETE /cuisines/{id}` не удаляет рецепты | 10 |

---

## Что проверит преподаватель

- `POST /cuisines/` с одинаковым именем дважды возвращает 409
- `POST /recipes/` с одинаковым заголовком создаёт второй рецепт с суффиксом в slug
- `PATCH /recipes/{id}` с `{"title": "New"}` меняет только title и пересчитывает slug
- `DELETE /cuisines/{id}` — рецепты остаются, у них `cuisine_id = NULL`
- Перезапуск сервера — данные сохранились
