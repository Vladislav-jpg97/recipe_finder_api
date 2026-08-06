# Урок 7 — Домашняя работа

## Recipe Finder API — JWT аутентификация

---

## Контекст

Продолжаем **Recipe Finder API**. Сейчас все эндпоинты открыты — любой может создавать, редактировать и удалять рецепты. Добавляем аутентификацию через JWT — такую же архитектуру как в DevTalks.

---

## Часть 1 — Зависимости

Добавь через Poetry:

```bash
poetry add "python-jose[cryptography]" "passlib[bcrypt]"
```

Обнови `.env` и `Settings`:

| Переменная | Тип | Описание |
| --- | --- | --- |
| `SECRET_KEY` | `str` | Секретный ключ подписи JWT |
| `ALGORITHM` | `str` | Алгоритм (значение по умолчанию: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | Время жизни access токена |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `int` | Время жизни refresh токена |

---

## Часть 2 — User модель

Создай Alembic миграцию и модель `User`. Поля:

| Поле | Тип | Ограничения |
| --- | --- | --- |
| `id` | `int` | PK, autoincrement |
| `email` | `str` | уникальный, не null |
| `username` | `str` | уникальный, не null |
| `hashed_password` | `str` | не null |
| `is_active` | `bool` | по умолчанию `True` |
| `created_at` | `datetime` | текущее время UTC |

---

## Часть 3 — Утилиты безопасности

Создай `app/core/security.py`. Функции которые должны быть:

| Функция | Что принимает | Что возвращает |
| --- | --- | --- |
| `hash_password` | `str` | хэшированный `str` |
| `verify_password` | `plain: str`, `hashed: str` | `bool` |
| `create_access_token` | `user_id: int` | JWT `str` |
| `create_refresh_token` | `user_id: int` | JWT `str` |
| `decode_token` | `token: str`, `expected_type: str` | `int` (user_id) |

Поведение `decode_token`: при невалидном токене или несовпадении `type` — выбрасывает `HTTPException(401)` с заголовком `WWW-Authenticate: Bearer`.

---

## Часть 4 — UserRepository и UserService

Создай `app/repositories/user_repo.py` с классом `UserRepository`.

Методы которые нужны:

| Метод | Что делает |
| --- | --- |
| `get_by_id(user_id)` | Возвращает `User` или `None` |
| `get_by_email(email)` | Возвращает `User` или `None` |
| `get_by_username(username)` | Возвращает `User` или `None` |
| `create(data)` | Создаёт пользователя, возвращает `User` |

Создай `app/services/user_service.py` с классом `UserService`.

Методы `UserService`:

- `register(data: UserCreate)` — проверяет уникальность email и username (409 если занято), создаёт пользователя через репозиторий
- `authenticate(email, password)` — находит по email, проверяет пароль через `verify_password`, проверяет `is_active`, возвращает `User`

Поведение: если email не найден или пароль неверен — одно сообщение для обоих случаев (безопасность).

---

## Часть 5 — Dependency get_current_user

Создай `app/dependencies/auth.py`.

Dependency `get_current_user`:

- Принимает `token` через `OAuth2PasswordBearer`
- Декодирует токен, получает `user_id`
- Загружает пользователя из БД
- Проверяет `is_active`
- Возвращает `User`

`tokenUrl` в `OAuth2PasswordBearer` должен совпадать с реальным URL логина.

---

## Часть 6 — Схемы аутентификации

Создай `app/schemas/auth.py`. Схемы:

| Схема | Поля |
| --- | --- |
| `LoginRequest` | `email: EmailStr`, `password: str` |
| `TokenResponse` | `access_token: str`, `refresh_token: str`, `token_type: str` |
| `RefreshRequest` | `refresh_token: str` |

Добавь `UserCreate` и `UserResponse` в `app/schemas/user.py`:

- `UserCreate`: `email`, `username` (3–50 символов), `password` (минимум 8 символов)
- `UserResponse`: `id`, `email`, `username`, `is_active`, `created_at` — без `hashed_password`

---

## Часть 7 — Роутер /auth

Создай `app/api/v1/auth.py` с роутером `prefix="/auth"`.

Эндпоинты:

| Метод | URL | Что делает | Код ответа |
| --- | --- | --- | --- |
| POST | `/register` | Регистрация нового пользователя | 201 |
| POST | `/login` | Логин, возвращает токены | 200 |
| POST | `/refresh` | Обновление access + refresh токенов | 200 |
| GET | `/me` | Профиль текущего пользователя | 200 |

`/me` — защищённый эндпоинт, требует валидный access токен.

Подключи роутер в `app/main.py`.

---

## Часть 8 — Защита эндпоинтов рецептов

Обнови роутер рецептов. Защити мутирующие операции:

- `POST /recipes/` — только для аутентифицированных пользователей
- `PUT /recipes/{id}` — только владелец рецепта
- `DELETE /recipes/{id}` — только владелец рецепта

Добавь поле `author_id` в модель `Recipe` (foreign key → `users.id`).

Поведение при попытке изменить чужой рецепт: `403 Forbidden`.

Для read-только эндпоинтов (`GET /recipes/`, `GET /recipes/{id}`) авторизация не нужна.

---

## Критерии оценки

| Критерий | Баллы |
| --- | --- |
| `hash_password` + `verify_password` через Passlib bcrypt | 10 |
| `create_access_token` и `create_refresh_token` с корректным `exp` | 10 |
| `decode_token` выбрасывает 401 при невалидном/истёкшем токене | 10 |
| `register` проверяет уникальность email и username (409) | 15 |
| `authenticate` одно сообщение для "нет пользователя" и "неверный пароль" | 10 |
| `get_current_user` проверяет `is_active` | 10 |
| `UserResponse` не содержит `hashed_password` | 10 |
| `POST /recipes/` требует авторизации, без токена — 401 | 15 |
| `PUT/DELETE /recipes/{id}` — 403 при попытке изменить чужой рецепт | 10 |

---

## Что проверит преподаватель

- `POST /auth/register` с уже существующим email → 409
- `POST /auth/login` с неверным паролем → 401 (не 404)
- `GET /auth/me` без токена → 401
- `GET /auth/me` с валидным токеном → профиль пользователя без пароля
- `POST /recipes/` без токена → 401
- `POST /recipes/` с токеном → 201, `author_id` назначен из токена
- `DELETE /recipes/{id}` с токеном другого пользователя → 403
