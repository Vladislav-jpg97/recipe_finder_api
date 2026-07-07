# Урок 1 — Домашняя работа

## Recipe Finder API

---

## Контекст

Ты строишь API для кулинарного приложения **Recipe Finder**. Это отдельный проект — не DevTalks. На протяжении курса домашние работы будут развивать его: в уроке 2 добавим Pydantic валидаторы, в уроке 3 — базу данных. К концу блога у тебя будет два полноценных проекта в портфолио.

Сегодня: FastAPI + данные прямо в коде. БД добавим позже.

---

## Часть 1 — Подготовка

Создай проект через Poetry (как делали с DevTalks на уроке):

```bash
mkdir recipe-finder && cd recipe-finder
poetry init --name recipe-finder --python "^3.12" --no-interaction
poetry add fastapi "uvicorn[standard]"
poetry shell
```

Структура — сразу правильная, как в DevTalks:

```text
recipe-finder/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── recipes.py
└── pyproject.toml
```

---

## Часть 2 — Данные

В `app/api/v1/recipes.py` создай список `RECIPES` с минимум 8 рецептами из разных кухонь. Каждый рецепт — словарь со следующими полями:

| Поле | Тип | Пример |
| --- | --- | --- |
| `id` | int | `1` |
| `title` | str | `"Паста Карбонара"` |
| `slug` | str | `"pasta-carbonara"` |
| `cuisine` | str | `"italian"` |
| `difficulty` | str | `"easy"` / `"medium"` / `"hard"` |
| `cooking_time` | int | минуты, `30` |
| `servings` | int | `2` |
| `calories_per_serving` | int | `620` |
| `ingredients` | list[str] | `["спагетти", "бекон"]` |
| `is_vegetarian` | bool | `False` |
| `rating` | float | `4.8` |

Возьми рецепты из разных кухонь: итальянская, японская, грузинская, мексиканская и т.д.

---

## Часть 3 — Эндпоинты (обязательно)

Реализуй следующие эндпоинты. Правильный порядок объявления маршрутов — на твоей ответственности (вспомни урок про route ordering).

### 3.1 Список рецептов

```text
GET /api/v1/recipes/
```

Query параметры для фильтрации и сортировки:

- `cuisine` — фильтр по кухне
- `difficulty` — фильтр по сложности
- `is_vegetarian` — только вегетарианские
- `max_time` — не дольше N минут
- `sort_by` — поле для сортировки: `rating`, `cooking_time`, `calories` (по умолчанию `rating`)

### 3.2 Один рецепт

```text
GET /api/v1/recipes/{slug}
```

Если рецепт не найден — 404.

### 3.3 Рецепты по ингредиенту

```text
GET /api/v1/recipes/by-ingredient/{ingredient}
```

Поиск без учёта регистра, частичное совпадение (`"томат"` найдёт `"черри томаты"`).

### 3.4 Случайный рецепт

```text
GET /api/v1/recipes/random
```

Query параметры (необязательные):

- `cuisine` — случайный из конкретной кухни
- `is_vegetarian` — только из вегетарианских

### 3.5 Статистика

```text
GET /api/v1/recipes/stats
```

Ожидаемая структура ответа:

```json
{
    "total": 8,
    "by_cuisine": {"italian": 2, "greek": 1},
    "by_difficulty": {"easy": 3, "medium": 4, "hard": 1},
    "vegetarian_count": 3,
    "average_rating": 4.3,
    "fastest_recipe": "Греческий салат",
    "slowest_recipe": "Говяжье рагу"
}
```

---

## Часть 4 — Response Models (обязательно)

Создай три Pydantic схемы и используй `response_model` во всех эндпоинтах.

**RecipeBrief** — краткая информация для списка:

- `id`, `title`, `slug`, `cuisine`, `difficulty`, `cooking_time`, `is_vegetarian`, `rating`

**RecipeDetail** — полная информация для одного рецепта:

- все поля `RecipeBrief` плюс `servings`, `calories_per_serving`, `ingredients`

**RecipeStats** — статистика:

- `total`, `by_cuisine`, `by_difficulty`, `vegetarian_count`, `average_rating`, `fastest_recipe`, `slowest_recipe`

Подбери правильные Python типы для каждого поля сам.

---

## Часть 5 — Бонус (необязательно)

### 5.1 Калькулятор порций

```text
GET /api/v1/recipes/{slug}/scale?servings=4
```

Пересчитать `calories_per_serving` под заданное количество порций.

### 5.2 Поиск по нескольким ингредиентам

```text
GET /api/v1/recipes/by-ingredients/?ingredients=яйца&ingredients=бекон
```

Найти рецепты где присутствуют **все** перечисленные ингредиенты одновременно.

Подсказка: FastAPI принимает повторяющиеся query параметры как список — изучи как аннотировать `list[str]` для query параметра.

### 5.3 Похожие рецепты

```text
GET /api/v1/recipes/{slug}/similar
```

До 3 рецептов той же кухни, исключая текущий.

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| Все 5 эндпоинтов работают корректно | 50 |
| `response_model` используется во всех эндпоинтах | 15 |
| Правильные HTTP статус коды (201, 404 и др.) | 10 |
| Читаемый код, осмысленные имена функций | 10 |
| Минимум 8 рецептов из разных кухонь | 5 |
| Swagger UI показывает все эндпоинты | 5 |
| Бонусные задания | +15 |

---

## Что проверит преподаватель

- `uvicorn app.main:app` запускается без ошибок
- `GET /api/v1/recipes/?cuisine=italian` возвращает только итальянские рецепты
- `GET /api/v1/recipes/несуществующий-slug` возвращает 404
- `GET /api/v1/recipes/by-ingredient/Томат` (с заглавной) находит рецепты с `томат`
- `GET /api/v1/recipes/stats` возвращает корректную статистику по всем рецептам
- Swagger UI доступен по `/docs`
