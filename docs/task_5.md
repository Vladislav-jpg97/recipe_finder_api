# Урок 5 — Домашняя работа

## Recipe Finder API — Ингредиенты и отзывы

---

## Контекст

Продолжаем **Recipe Finder API**. До этого поле `ingredients` хранило список ингредиентов как JSON-строку в одной колонке — это неудобно для поиска по ингредиентам. Сейчас переводим ингредиенты в отдельную таблицу и добавляем систему отзывов.

---

## Часть 1 — Модель Ingredient (many-to-many)

Создай `app/models/ingredient.py` с моделью ингредиента. Поля:

| Поле | Тип Python | Ограничения |
| --- | --- | --- |
| `id` | `int` | primary key |
| `name` | `str` | max 100, unique, indexed |
| `slug` | `str` | max 110, unique, indexed |

Создай ассоциативную таблицу `recipe_ingredients` — только две колонки:

| Колонка | Тип | Особенности |
| --- | --- | --- |
| `recipe_id` | ForeignKey `recipes.id` | primary key, CASCADE при удалении рецепта |
| `ingredient_id` | ForeignKey `ingredients.id` | primary key, CASCADE при удалении ингредиента |

Обнови модель `Recipe`:

- Удали поле `ingredients: str`
- Добавь relationship `ingredients` к `Ingredient` через `recipe_ingredients`

Создай Alembic миграцию и примени её.

---

## Часть 2 — Модель RecipeReview (без вложенности)

Создай `app/models/review.py` с моделью отзыва. Поля:

| Поле | Тип Python | Ограничения |
| --- | --- | --- |
| `id` | `int` | primary key |
| `recipe_id` | `int` | ForeignKey `recipes.id`, CASCADE |
| `author_name` | `str` | max 100 |
| `rating` | `int` | от 1 до 5 (ограничение через `CheckConstraint`) |
| `content` | `str` | Text, min 10 символов |
| `created_at` | `datetime` | server_default=func.now() |

`CheckConstraint` на поле `rating` чтобы в БД нельзя было вставить значение вне 1–5.

---

## Часть 3 — IngredientRepository

Создай `app/repositories/ingredient_repo.py` с `IngredientRepository`. Методы:

| Метод | Описание |
| --- | --- |
| `get_all` | SELECT всех ингредиентов |
| `get_by_id` | SELECT по id |
| `get_by_slug` | SELECT по slug |
| `get_by_ids` | SELECT по списку id: `WHERE id IN (...)` |
| `add` | flush + refresh |
| `delete` | delete + flush |

---

## Часть 4 — RecipeReviewRepository

Создай `app/repositories/review_repo.py` с `RecipeReviewRepository`. Методы:

| Метод | Описание |
| --- | --- |
| `get_by_recipe` | SELECT всех отзывов для рецепта, ORDER BY created_at DESC |
| `get_by_id` | SELECT по id |
| `add` | flush + refresh |
| `delete` | delete + flush |

---

## Часть 5 — IngredientService

Поведение:

### create

Генерирует slug из name. Если slug занят — 409. Коммитит.

### delete

Удаляет ингредиент. Связи в `recipe_ingredients` удалятся через CASCADE. Коммитит.

---

## Часть 6 — RecipeService: обновление many-to-many

Обнови `RecipeService`. Добавь в метод `create` поддержку `ingredient_ids`:

- Принимает список id ингредиентов
- Загружает объекты `Ingredient` по ids через `IngredientRepository.get_by_ids`
- Присваивает `recipe.ingredients = [список объектов]`

Обнови метод `update`:

- Если в данных есть `ingredient_ids` — обновить список ингредиентов рецепта
- Просто присвой `recipe.ingredients = [новые объекты]` — SQLAlchemy обновит связи

---

## Часть 7 — RecipeReviewService

Поведение:

### get_by_recipe

Принимает `recipe_id`. Возвращает все отзывы.

### create

- Принимает `recipe_id`, `author_name`, `rating`, `content`
- Создаёт отзыв
- Если `rating` вне 1–5 — 400 Bad Request (можно проверить в Pydantic схеме)
- Коммитит

### delete

Принимает `review_id`. Удаляет. Коммитит. Если не найден — 404.

---

## Часть 8 — Роутеры

### app/api/v1/ingredients.py

| Метод | URL | Статус | Описание |
| --- | --- | --- | --- |
| GET | `/ingredients/` | 200 | Список всех ингредиентов |
| POST | `/ingredients/` | 201 | Создать ингредиент |
| DELETE | `/ingredients/{ingredient_id}` | 204 | Удалить ингредиент |

### Обнови app/api/v1/recipes.py

`RecipeCreate` и `RecipeUpdate` теперь принимают `ingredient_ids: list[int]`.

### app/api/v1/reviews.py

| Метод | URL | Статус | Описание |
| --- | --- | --- | --- |
| GET | `/recipes/{recipe_id}/reviews` | 200 | Отзывы к рецепту |
| POST | `/recipes/{recipe_id}/reviews` | 201 | Добавить отзыв |
| DELETE | `/reviews/{review_id}` | 204 | Удалить отзыв |

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| Модель `Ingredient` + ассоциативная таблица + миграция | 20 |
| `RecipeService.create` сохраняет список ингредиентов | 15 |
| `RecipeService.update` обновляет список ингредиентов | 15 |
| Модель `RecipeReview` с `CheckConstraint` для rating | 15 |
| `RecipeReviewService` с валидацией rating 1–5 | 15 |
| Роутеры с правильными статус-кодами | 10 |
| CASCADE удаление связей при удалении ингредиента | 10 |

---

## Что проверит преподаватель

- Создать рецепт с `ingredient_ids=[1, 2]`, получить рецепт — видим список ингредиентов
- Обновить рецепт с `ingredient_ids=[3]` — старые ингредиенты заменились
- Удалить ингредиент — рецепты с ним не удалились, просто убрана связь
- `POST /recipes/{id}/reviews` с `rating=6` возвращает 400
- `GET /recipes/{id}/reviews` возвращает отзывы от новых к старым
