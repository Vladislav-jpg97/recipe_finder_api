# Урок 8 — Домашняя работа

## Recipe Finder API — Redis кэширование

---

## Контекст

Продолжаем **Recipe Finder API**. Добавляем Redis кэширование — такую же архитектуру как в DevTalks. После этого урока Recipe Finder умеет кэшировать списки рецептов, детальные страницы и справочники, инвалидировать кэш при изменениях.

---

## Часть 1 — Зависимости и конфигурация

Добавь Redis через Poetry:

```bash
poetry add "redis[asyncio]"
```

Запусти Redis:

```bash
docker run -d --name recipe_redis -p 6379:6379 redis:7-alpine
```

Добавь в `.env` и `Settings`:

| Переменная | Значение по умолчанию |
| --- | --- |
| `REDIS_URL` | `redis://localhost:6379` |

---

## Часть 2 — CacheService

Создай `app/core/cache.py` по образу DevTalks. Методы которые нужны:

| Метод | Сигнатура | Описание |
| --- | --- | --- |
| `get` | `(key: str) → Any\|None` | Читает и десериализует из Redis |
| `set` | `(key: str, value: Any, ttl: int = 300) → None` | Сериализует и сохраняет с TTL |
| `delete` | `(key: str) → None` | Удаляет один ключ |
| `delete_pattern` | `(pattern: str) → None` | Удаляет все ключи по паттерну |
| `close` | `() → None` | Закрывает соединение |

Синглтон `cache = CacheService()` — один экземпляр на весь процесс.

Подключи `cache.close()` в `lifespan` `app/main.py`.

---

## Часть 3 — Стратегия ключей

Определи ключи кэша для Recipe Finder. Используй формат `entity:action:params`:

| Что кэшировать | Ключ | TTL |
| --- | --- | --- |
| Список рецептов с параметрами | `recipes:list:page=N:size=N:...` | 5 мин |
| Детальный рецепт | `recipes:detail:{id}` | 10 мин |
| Список кухонь | `cuisines:list` | 1 час |

---

## Часть 4 — Кэш в RecipeRepository

Обнови `RecipeRepository`:

Метод `get_paginated`:

- Перед запросом к БД — строит ключ кэша из всех параметров pagination и filters
- При cache HIT — возвращает данные из Redis напрямую
- При cache MISS — делает запрос к БД, сериализует через `Page.model_dump()`, сохраняет в Redis
- TTL: 5 минут

Метод `get_by_id`:

- Ключ: `recipes:detail:{recipe_id}`
- При HIT — возвращает из Redis
- При MISS — запрос к БД с `selectinload` для связей, сериализует через `RecipeDetailResponse.model_dump()`, сохраняет
- TTL: 10 минут

---

## Часть 5 — Кэш в CuisineRepository

Метод `get_all` в `CuisineRepository`:

- Ключ: `cuisines:list`
- TTL: 1 час
- При создании новой кухни — инвалидация ключа

---

## Часть 6 — Инвалидация в RecipeService

Добавь инвалидацию после каждой мутации:

- После `create`: удалить `recipes:list:*`
- После `update`: удалить `recipes:detail:{id}` и `recipes:list:*`
- После `delete`: удалить `recipes:detail:{id}` и `recipes:list:*`

Инвалидация должна происходить только после успешного изменения в БД.

---

## Часть 7 — Refresh Token Whitelist (бонус)

Реализуй хранение refresh токенов в Redis — whitelist подход.

Поведение:

- При `POST /auth/login`: сохрани refresh_token в Redis
  - ключ: `refresh:{token_value}`
  - значение: `str(user_id)`
  - TTL: `REFRESH_TOKEN_EXPIRE_DAYS * 86400`

- При `POST /auth/refresh`: перед выдачей нового токена проверь что старый refresh_token есть в Redis. Если нет — 401. После проверки удали старый токен и сохрани новый.

- При `POST /auth/logout` (новый эндпоинт): удали refresh_token из Redis

Поведение logout:

- Принимает `refresh_token` в теле
- Удаляет ключ из Redis
- Возвращает `{"message": "Logged out"}`

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| `CacheService` с корректными методами get/set/delete/delete_pattern | 15 |
| `cache.close()` вызван в lifespan shutdown | 5 |
| Ключ кэша `recipes:list:*` уникален для каждой комбинации параметров | 15 |
| `get_by_id` кэшируется через `RecipeDetailResponse.model_dump()` | 15 |
| Инвалидация при create/update/delete | 20 |
| `cuisines:list` кэшируется на 1 час с инвалидацией | 10 |
| Бонус: refresh token whitelist в Redis | 20 |

---

## Что проверит преподаватель

- Первый `GET /recipes/` — cache MISS, запрос к БД
- Второй `GET /recipes/` с теми же параметрами — cache HIT, нет запроса к БД
- `POST /recipes/` + `GET /recipes/` — данные обновились (кэш инвалидирован)
- `PUT /recipes/{id}` + `GET /recipes/{id}` — детальная страница обновилась
- `GET /cuisines/` второй раз подряд — из кэша (без запроса к БД)
- В Redis CLI `KEYS *` — видны ключи с правильными именами
