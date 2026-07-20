# Урок 6 — Домашняя работа

## Recipe Finder API — Поиск, пагинация и фильтрация

---

## Контекст

Продолжаем **Recipe Finder API**. Сейчас `GET /recipes/` возвращает все рецепты без ограничений. Добавляем пагинацию с метаданными, поиск по названию, фильтрацию и сортировку — как делали в DevTalks.

---

## Часть 1 — PaginationParams

Скопируй `PaginationParams` и `Page[T]` из DevTalks в `app/schemas/pagination.py`. Это универсальные утилиты — они не привязаны к Recipe.

Убедись что:

- `Page[T]` использует `Generic[T]` правильно
- `PaginationParams` имеет свойства `offset` и `limit`
- Метод `Page.create()` корректно считает `pages` (ceiling division)
- `has_next` и `has_prev` корректны при `total=0`

---

## Часть 2 — RecipeFilters

Создай класс `RecipeFilters` в `app/schemas/recipe.py`. Это обычный Python класс с `__init__`, не BaseModel.

Параметры фильтрации:

| Параметр | Тип | По умолчанию | Описание |
| --- | --- | --- | --- |
| `search` | `str` или `None` | `None` | Поиск по `title` |
| `cuisine_id` | `int` или `None` | `None` | Фильтр по кухне |
| `is_vegetarian` | `bool` или `None` | `None` | Только вегетарианские |
| `difficulty` | `str` или `None` | `None` | Уровень сложности |
| `max_cooking_time` | `int` или `None` | `None` | Максимальное время приготовления (мин) |
| `sort_by` | `str` | `"created_at"` | Поле сортировки: `created_at`, `rating`, `cooking_time` |
| `sort_order` | `str` | `"desc"` | Направление: `asc` или `desc` |

Используй `Query(enum=[...])` для `sort_by` и `sort_order`.

---

## Часть 3 — RecipeRepository: метод get_paginated

Обнови `RecipeRepository`. Добавь метод `get_paginated` который принимает `PaginationParams` и `RecipeFilters`.

Поведение метода:

- Строит base query с `selectinload(Recipe.cuisine)` и `selectinload(Recipe.ingredients)`
- Применяет фильтр `ILIKE` по `title` если `search` задан
- Фильтрует по `cuisine_id` если задан
- Фильтрует по `is_vegetarian` если задан
- Фильтрует по `difficulty` если задан (точное совпадение)
- Фильтрует по `cooking_time <= max_cooking_time` если `max_cooking_time` задан
- Считает `total` через `select(func.count()).select_from(query.subquery())` — ДО пагинации
- Применяет сортировку через `getattr(Recipe, sort_by, Recipe.created_at)`
- Применяет `offset` и `limit`
- Возвращает `Page.create(items=..., total=..., params=pagination)`

---

## Часть 4 — RecipeService

Обнови `RecipeService`. Добавь метод `get_paginated`:

- Принимает `PaginationParams` и `RecipeFilters`
- Делегирует в `RecipeRepository.get_paginated`
- Возвращает `Page[RecipeResponse]` (но возвращать нужно `Page` — FastAPI сам конвертирует)

---

## Часть 5 — Обновить роутер GET /recipes/

Обнови эндпоинт `GET /recipes/` в `app/api/v1/recipes.py`:

- `response_model` должен быть `Page[RecipeResponse]`
- Параметры: `pagination: PaginationParams = Depends()` и `filters: RecipeFilters = Depends()`
- Вызывает `service.get_paginated(pagination, filters)`

---

## Часть 6 — GET /recipes/top-rated

Добавь эндпоинт `GET /recipes/top-rated` который возвращает топ-10 рецептов по рейтингу.

Поведение:

- Параметр `limit: int` — значение по умолчанию 10, максимум 50
- Возвращает `list[RecipeResponse]`
- Сортировка по `rating DESC`
- Только рецепты с `rating > 0`

Убедись что этот маршрут объявлен ДО `/{recipe_id}` в роутере.

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| `Page[T]` с корректным `Generic[T]` | 15 |
| `PaginationParams` с `offset` и `limit` свойствами | 10 |
| `RecipeFilters` с `Query(enum=...)` для sort_by | 15 |
| `get_paginated` считает total ДО LIMIT | 20 |
| `ILIKE` для регистронезависимого поиска | 15 |
| `GET /recipes/top-rated` объявлен ДО `/{id}` | 10 |
| `Page` содержит корректные `has_next`, `has_prev`, `pages` | 15 |

---

## Что проверит преподаватель

- `GET /recipes/?page=1&size=3` — возвращает max 3 рецепта, `total` = полное количество
- `GET /recipes/?search=pasta` — находит "Pasta Carbonara" и "Spaghetti" (регистронезависимо)
- `GET /recipes/?is_vegetarian=true&sort_by=rating&sort_order=asc` — только вегетарианские, по рейтингу
- `GET /recipes/?max_cooking_time=30` — только быстрые рецепты
- `GET /recipes/top-rated` — не вызывает 422 (не интерпретируется как `recipe_id`)
- `has_next=false` на последней странице, `has_prev=false` на первой
