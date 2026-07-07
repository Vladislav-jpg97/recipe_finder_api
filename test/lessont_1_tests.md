# Урок 1 — Тесты по теории

---

## Ответы :  Ставлю + 

## Часть 1 — Теория (выбор ответа)

**1. Что такое ASGI?**

- A) Библиотека для работы с базами данных
- B) Стандарт для асинхронных Python веб-серверов +
- C) Инструмент для генерации документации
- D) Менеджер пакетов Python

---

**2. Какой из этих URL содержит path параметр, а не query параметр?**

- A) `/posts?id=42`
- B) `/posts/42` +
- C) `/posts#42`
- D) `/posts&id=42`

---

**3. Что произойдёт при запросе `GET /posts/abc`, если эндпоинт объявлен как `get_post(post_id: int)`?**

- A) FastAPI вернёт `post_id = 0` как значение по умолчанию
- B) FastAPI вызовет функцию с `post_id = "abc"`
- C) FastAPI автоматически вернёт `422 Unprocessable Entity` +
- D) FastAPI вернёт `500 Internal Server Error`

---

**4. Зачем нужен `--reload` при запуске через uvicorn?**

- A) Для автоматической документации
- B) Для увеличения производительности
- C) Для автоматического перезапуска сервера при изменении файлов +
- D) Для включения режима отладки с подробными ошибками

---

**5. У тебя есть два маршрута. Какой порядок правильный?**

```python
# Вариант A:
@app.get("/posts/drafts")
@app.get("/posts/{post_id}")

# Вариант B:
@app.get("/posts/{post_id}")
@app.get("/posts/drafts")
```

- A) Вариант A +
- B) Вариант B
- C) Порядок не важен, FastAPI разберётся сам
- D) Оба варианта неправильные

---

**6. Что делает `response_model` в эндпоинте?**

- A) Ускоряет сериализацию JSON
- B) Фильтрует поля ответа по схеме и генерирует документацию +
- C) Валидирует входящий запрос
- D) Автоматически добавляет токен авторизации

---

**7. Какой HTTP статус код нужно вернуть при успешном создании ресурса (POST)?**

- A) 200 OK
- B) 201 Created +
- C) 204 No Content
- D) 202 Accepted

---

**8. Как объявить необязательный query параметр `search` типа `str` который по умолчанию `None`?**

- A) `search: str`
- B) `search: str = ""`
- C) `search: str | None = None` +
- D) `search: Optional = None`

---

## Часть 2 — Логические и алгоритмические задачи

**9. Порядок маршрутов**

Посмотри на код и скажи: что вернёт запрос `GET /users/me`? Почему?

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/users/me")
async def get_me():
    return {"user": "current"}
```
Ответ : 

вернет INT так как при написание кода нужно соблюдать правила 
Эндпоинтый со статическими данными пишутся выше чем с динамическими данными


---

**10. Что выведет следующий код?**

Определи какой HTTP метод и путь у каждого эндпоинта, и по какому URL к нему обратиться.

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/")
async def list_articles():
    return []

@router.get("/{slug}")
async def get_article(slug: str):
    return {"slug": slug}

@router.post("/")
async def create_article():
    return {"created": True}
app.include_router(router, prefix="/api/v1")
```

Заполни таблицу:
Ответ : 

| Функция | HTTP метод | Полный URL |
|---|---|---|
| `list_articles` | get | api/v1/articles/ |
| `get_article` | get | api/v1/articles/{slug}/ |
| `create_article` | post | api/v1/articles/ |


---

**11. Алгоритм: найди баг**

Следующий код содержит **две ошибки**. Найди их и объясни как исправить.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    return {"post_id": post_id}

@app.get("/posts/top")
async def get_top_posts(limit = 10):
    return {"posts": []}

@app.delete("/posts/{post_id}", status_code=200)
async def delete_post(post_id: int):
    return {"deleted": True}
```
Ответ : 
№ 1 - то что динамический эндпонт стоит выше статического
№ 2 - при удаление статус код должен быть 204 "delete_post"

---

## Часть 3 — Открытые вопросы

**12.** Объясни своими словами: в чём разница между `async def` и `def` в контексте FastAPI? Когда ты бы использовал каждый вариант?

Ответ : 
Если функция делает тяжёлые задачи (запросы к БД, обращения к другим API), мы пишем async def и используем await.

Если у нас обычные вычисления или старые библиотеки без поддержки асинхронности (например, старый psycopg2), мы пишем обычный def. FastAPI сам запустит её в отдельном потоке (Thread pool), чтобы она не тормозила весь сервер.


---

**13.** У тебя есть эндпоинт:

```python
@app.get("/search")
async def search(q: str, page: int = 1, size: int = 20):
    ...
```

Напиши три разных URL которые корректно обратятся к этому эндпоинту. Один из них должен использовать только обязательный параметр.
Ответ:
http://127.0.0.1:8000/search?q=fastap
http://127.0.0.1:8000/search?q=fastapi&page=2
http://127.0.0.1:8000/search?q=fastapi&page=2&size=50

---

**14.** Почему в REST API принято использовать разные HTTP методы (`GET`, `POST`, `DELETE`) вместо того чтобы кодировать действие в URL (`/posts/delete/42`, `/posts/create`)?
для простоты работы и понимания кода , вместо сотен придуманных путей мы просто берем URL , а само действие определяем методом
---

**15.** Представь что ты проектируешь API для платформы DevTalks. Какие эндпоинты тебе понадобятся для работы с постами? Напиши минимум 5 с указанием HTTP метода и пути.
Ответ: 

Получить список всех постов
GET /post

Получить один конкретный пост по ID.
GET /posts/{post_id} 

Создать новый пост
POST /posts 

Полностью обновить пост.
PUT /posts/{post_id} 

Удалить пост.
DELETE /posts/{post_id}  
