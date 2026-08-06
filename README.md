# 🍳 Recipe Finder API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy 2.0" />
  <img src="https://img.shields.io/badge/Alembic-migrations-6BA539?style=flat-square" alt="Alembic" />
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic v2" />
  <img src="https://img.shields.io/badge/Poetry-dependency%20management-60A5FA?style=flat-square&logo=poetry&logoColor=white" alt="Poetry" />
  <img src="https://img.shields.io/badge/JWT-auth-000000?style=flat-square&logo=jsonwebtokens&logoColor=white" alt="JWT" />
  <img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/status-learning%20project-yellow?style=flat-square" alt="Status" />
</p>

<p align="center">
  A production-style <strong>FastAPI</strong> backend for a cooking/recipe discovery app, built incrementally
  across an 11-lesson backend course — from a plain in-memory API to a fully containerized,
  authenticated, cached, and paginated service.
</p>

---

## 📖 About

**Recipe Finder API** is a learning project built lesson-by-lesson as backend homework. It's a
companion project to a parallel "DevTalks" course project, used to practice the same concepts
independently on a different domain. Each lesson adds a real production concern on top of the
previous one, so the git history (or lesson folders) doubles as a changelog of backend
architecture decisions.

> ⚠️ This is a study/portfolio project. Some values (secrets, sample data) are for local
> development only and should never be used in a real production deployment as-is.

## 🧭 Table of Contents

- [Feature Overview](#-feature-overview)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Learning Path / Lesson Map](#-learning-path--lesson-map)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Option A — Docker Compose (recommended)](#option-a--docker-compose-recommended)
  - [Option B — Local (Poetry)](#option-b--local-poetry)
- [Environment Variables](#-environment-variables)
- [API Overview](#-api-overview)
- [Database Schema](#-database-schema)
- [Caching Strategy](#-caching-strategy)
- [Authentication](#-authentication)
- [Makefile Commands](#-makefile-commands)
- [Roadmap / Not Yet Covered](#-roadmap--not-yet-covered)
- [License](#-license)

---

## ✨ Feature Overview

| Area | Status | Details |
| --- | :---: | --- |
| REST API (CRUD) | ✅ | Recipes, cuisines, ingredients, reviews |
| Validation | ✅ | Pydantic v2 schemas, custom validators, normalization |
| Persistence | ✅ | PostgreSQL via async SQLAlchemy 2.0 (`Mapped`/`mapped_column`) |
| Migrations | ✅ | Alembic, async engine, autogenerate |
| Layered architecture | ✅ | Router → Service → Repository → Model |
| Relational modeling | ✅ | 1-to-many (`Recipe → Cuisine`), many-to-many (`Recipe ↔ Ingredient`) |
| Reviews | ✅ | 1-to-many reviews per recipe, DB-level `CheckConstraint` |
| Pagination & filtering | ✅ | Generic `Page[T]`, search, sorting, `ILIKE` search |
| Auth | ✅ | JWT access + refresh tokens, bcrypt password hashing |
| Authorization | ✅ | Ownership checks (`403`) on mutation endpoints |
| Caching | ✅ | Redis, key-based invalidation, refresh-token whitelist |
| Containerization | ✅ | Multi-layer Dockerfile, non-root user, healthcheck |
| Orchestration | ✅ | Docker Compose (Postgres + Redis + migrate + web) |
| Automated tests | ⏳ | Not part of the homework scope yet |
| CI/CD | ⏳ | Not part of the homework scope yet |

---

## 🛠 Tech Stack

**Core**
- [FastAPI](https://fastapi.tiangolo.com/) — async web framework
- [Pydantic v2](https://docs.pydantic.dev/) — request/response validation & settings
- [Uvicorn](https://www.uvicorn.org/) — ASGI server

**Data layer**
- [PostgreSQL 16](https://www.postgresql.org/) — primary datastore
- [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (async, `asyncpg` driver) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — schema migrations

**Auth & security**
- [python-jose](https://github.com/mpdavis/python-jose) — JWT encode/decode
- [passlib\[bcrypt\]](https://passlib.readthedocs.io/) — password hashing

**Caching**
- [Redis 7](https://redis.io/) (`redis[asyncio]`) — response caching + refresh-token whitelist

**Tooling / Infra**
- [Poetry](https://python-poetry.org/) — dependency & environment management
- Docker & Docker Compose — packaging and local orchestration

---

## 🏗 Project Architecture

The API follows a classic layered/clean architecture, introduced starting from **Lesson 4**:

```
Client
  │
  ▼
Router (app/api/v1/*.py)        — HTTP layer: parses request, calls service, sets status codes
  │
  ▼
Service (app/services/*.py)      — business logic: slug generation, uniqueness checks,
  │                                 authorization rules, cache invalidation
  ▼
Repository (app/repositories/*.py) — SQL layer: SELECT/INSERT/UPDATE/DELETE via SQLAlchemy
  │
  ▼
Model (app/models/*.py)          — SQLAlchemy ORM models / DB schema
```

Dependency injection is done via FastAPI's `Depends`, with a factory function per router
(`get_recipe_service`, `get_cuisine_service`, …) that wires up
`AsyncSession → Repository → Service`.

---

## 🗺 Learning Path / Lesson Map

Each lesson built directly on top of the previous one's codebase:

| Lesson | Topic | What was added |
| :---: | --- | --- |
| 1 | FastAPI fundamentals | Project scaffolding, in-memory data, first 5 endpoints, `response_model` schemas |
| 2 | Pydantic & validation | `schemas.py`, `RecipeCreate`/`RecipeUpdate`, field validators, `pydantic-settings` |
| 3 | Database basics | PostgreSQL, SQLAlchemy 2.0 model, Alembic, async `get_db`, `seed.py` |
| 4 | Repository/Service pattern | `Cuisine` model + FK, `RecipeRepository`, `CuisineRepository`, services, DI |
| 5 | Relational modeling | `Ingredient` (many-to-many), `RecipeReview` (1-to-many), `CheckConstraint` |
| 6 | Pagination & search | Generic `Page[T]`, `PaginationParams`, `RecipeFilters`, `ILIKE` search, `top-rated` |
| 7 | Authentication | `User` model, JWT access/refresh tokens, bcrypt, ownership-based `403` |
| 8 | Caching | Redis `CacheService`, cache-aside pattern, invalidation, refresh-token whitelist |
| 10 | Docker | Multi-stage-ready `Dockerfile`, `.dockerignore`, `/health` endpoint, `Makefile` |
| 11 | Docker Compose | Full stack orchestration: Postgres + Redis + `migrate` + `web`, healthchecks |

> Lesson 9 focused on non-API material (e.g. testing/theory) and didn't produce homework
> artifacts for this repo — hence the jump from Lesson 8 to Lesson 10 above.

---

## 📁 Project Structure

```text
recipe-finder/
├── app/
│   ├── main.py                  # FastAPI app, lifespan, /health
│   ├── config.py                # pydantic-settings Settings
│   ├── database.py              # async engine, sessionmaker, get_db
│   │
│   ├── api/v1/
│   │   ├── auth.py              # /auth/register, /login, /refresh, /me, /logout
│   │   ├── recipes.py           # /recipes CRUD, pagination, top-rated
│   │   ├── cuisines.py          # /cuisines CRUD
│   │   ├── ingredients.py       # /ingredients CRUD
│   │   └── reviews.py           # /recipes/{id}/reviews, /reviews/{id}
│   │
│   ├── models/
│   │   ├── recipe.py            # Recipe (FK: cuisine, author; M2M: ingredients)
│   │   ├── cuisine.py           # Cuisine
│   │   ├── ingredient.py        # Ingredient + recipe_ingredients assoc. table
│   │   ├── review.py            # RecipeReview (CheckConstraint 1–5 rating)
│   │   └── user.py              # User
│   │
│   ├── repositories/
│   │   ├── recipe_repo.py       # SQL queries + Redis cache-aside for recipes
│   │   ├── cuisine_repo.py
│   │   ├── ingredient_repo.py
│   │   ├── review_repo.py
│   │   └── user_repo.py
│   │
│   ├── services/
│   │   ├── recipe_service.py    # slug generation, cache invalidation, ownership
│   │   ├── cuisine_service.py
│   │   ├── ingredient_service.py
│   │   ├── review_service.py
│   │   └── user_service.py      # register / authenticate
│   │
│   ├── schemas/
│   │   ├── recipe.py            # RecipeCreate/Update/Response, RecipeFilters
│   │   ├── pagination.py        # PaginationParams, Page[T]
│   │   ├── auth.py              # LoginRequest, TokenResponse, RefreshRequest
│   │   └── user.py              # UserCreate, UserResponse
│   │
│   ├── core/
│   │   ├── security.py          # hash/verify password, JWT create/decode
│   │   └── cache.py             # CacheService (Redis get/set/delete/delete_pattern)
│   │
│   └── dependencies/
│       └── auth.py              # get_current_user (OAuth2PasswordBearer)
│
├── migrations/                  # Alembic (async env.py)
├── seed.py                      # Seeds initial recipes into Postgres
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── .env / .env.example
├── .env.docker / .env.docker.example
├── .dockerignore
└── pyproject.toml
```

---

## 🚀 Getting Started

### Option A — Docker Compose (recommended)

Spins up PostgreSQL, Redis, runs migrations, then starts the API — one command.

```bash
git clone <your-repo-url> recipe-finder
cd recipe-finder

cp .env.docker.example .env.docker   # fill in real values
make up                              # build + start full stack in background
```

Then verify:

```bash
curl http://localhost:8000/health     # {"status": "ok"}
open  http://localhost:8000/docs      # Swagger UI
```

Other useful commands:

```bash
make logs     # follow web service logs
make psql     # open a psql shell against the running Postgres
make down     # stop containers (keeps volumes/data)
make reset    # stop containers AND wipe volumes (full reset)
```

### Option B — Local (Poetry)

For active development without Docker.

```bash
git clone <your-repo-url> recipe-finder
cd recipe-finder

poetry install
poetry shell

cp .env.example .env          # fill in DATABASE_URL, REDIS_URL, SECRET_KEY, etc.

# run Postgres & Redis locally, or via standalone containers:
docker run -d --name recipe_redis -p 6379:6379 redis:7-alpine

alembic upgrade head
poetry run python seed.py     # optional: load sample recipes

uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`, docs at `http://localhost:8000/docs`.

---

## 🔐 Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | Async Postgres connection string | `postgresql+asyncpg://user:pass@localhost:5432/recipe_finder` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT signing secret | *(random string, keep private)* |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `APP_NAME` | App display name (Swagger title) | `Recipe Finder` |
| `DEBUG` | Debug mode flag | `False` |
| `DEFAULT_PAGE_SIZE` | Default pagination page size | `10` |
| `MAX_RECIPES` | Soft cap on stored recipes | `1000` |

Docker Compose uses a separate `.env.docker` file where `DATABASE_URL` / `REDIS_URL`
point at the **service names** (`postgres`, `redis`) instead of `localhost`.
`.env`, `.env.docker` and their real secrets are git-ignored — only the `.example` templates
are committed.

---

## 📡 API Overview

Interactive documentation is always available at **`/docs`** (Swagger UI) once the app is
running. High-level summary:

### Recipes
| Method | Endpoint | Auth | Description |
| --- | --- | :---: | --- |
| `GET` | `/api/v1/recipes/` | – | Paginated list, filters + search + sort |
| `GET` | `/api/v1/recipes/top-rated` | – | Top-rated recipes (`rating > 0`) |
| `GET` | `/api/v1/recipes/{id}` | – | Recipe detail |
| `GET` | `/api/v1/recipes/by-ingredient/{ingredient}` | – | Case-insensitive partial match |
| `GET` | `/api/v1/recipes/random` | – | Random recipe (optional filters) |
| `GET` | `/api/v1/recipes/stats` | – | Aggregate statistics |
| `POST` | `/api/v1/recipes/` | 🔒 | Create recipe (`author_id` from token) |
| `PATCH` | `/api/v1/recipes/{id}` | 🔒 owner | Partial update |
| `PUT` | `/api/v1/recipes/{id}` | 🔒 owner | Full update |
| `DELETE` | `/api/v1/recipes/{id}` | 🔒 owner | Delete recipe |

### Cuisines / Ingredients / Reviews
| Method | Endpoint | Auth | Description |
| --- | --- | :---: | --- |
| `GET` / `POST` | `/api/v1/cuisines/` | – / 🔒 | List / create cuisine |
| `DELETE` | `/api/v1/cuisines/{id}` | 🔒 | Delete cuisine (recipes keep, FK set null) |
| `GET` / `POST` | `/api/v1/ingredients/` | – / 🔒 | List / create ingredient |
| `DELETE` | `/api/v1/ingredients/{id}` | 🔒 | Delete ingredient (cascade on join table) |
| `GET` / `POST` | `/api/v1/recipes/{id}/reviews` | – / open | List / add review |
| `DELETE` | `/api/v1/reviews/{id}` | 🔒 | Delete review |

### Auth
| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Create account |
| `POST` | `/api/v1/auth/login` | Get access + refresh tokens |
| `POST` | `/api/v1/auth/refresh` | Rotate tokens (whitelist-checked) |
| `POST` | `/api/v1/auth/logout` | Revoke refresh token |
| `GET` | `/api/v1/auth/me` | Current user profile |

### System
| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Liveness probe, no DB dependency |

---

## 🗄 Database Schema

```
users                recipes                    cuisines
──────               ────────                   ─────────
id PK                id PK                       id PK
email UNIQUE         title                       name UNIQUE
username UNIQUE      slug UNIQUE                 slug UNIQUE
hashed_password      cuisine_id FK → cuisines    country_code
is_active             (ON DELETE SET NULL)
created_at           author_id FK → users
                      difficulty
                      cooking_time
                      servings
                      calories_per_serving
                      is_vegetarian
                      rating
                      created_at

ingredients           recipe_ingredients (M2M)    recipe_reviews
────────────          ───────────────────         ───────────────
id PK                 recipe_id FK (CASCADE)       id PK
name UNIQUE           ingredient_id FK (CASCADE)   recipe_id FK (CASCADE)
slug UNIQUE           (composite PK)               author_name
                                                    rating  CHECK (1–5)
                                                    content
                                                    created_at
```

**Relationship notes**
- `Recipe → Cuisine`: many-to-one, `ON DELETE SET NULL` (deleting a cuisine keeps its recipes).
- `Recipe ↔ Ingredient`: many-to-many via `recipe_ingredients`, both FKs `CASCADE`.
- `Recipe → RecipeReview`: one-to-many, `CASCADE` (deleting a recipe deletes its reviews).
- `rating` on `recipe_reviews` is enforced at the DB level with a `CheckConstraint (1–5)`,
  in addition to Pydantic-level validation.

---

## ⚡ Caching Strategy

Cache-aside pattern via a Redis-backed `CacheService`, introduced in Lesson 8.

| Cached resource | Key pattern | TTL | Invalidated on |
| --- | --- | :---: | --- |
| Recipe list (paginated + filtered) | `recipes:list:page=N:size=N:...` | 5 min | any recipe create/update/delete |
| Recipe detail | `recipes:detail:{id}` | 10 min | update/delete of that recipe |
| Cuisine list | `cuisines:list` | 1 hour | new cuisine created |
| Refresh token whitelist | `refresh:{token}` → `user_id` | `REFRESH_TOKEN_EXPIRE_DAYS` | used on `/auth/refresh`, `/auth/logout` |

All mutation endpoints invalidate the relevant keys **only after** a successful DB commit.

---

## 🔑 Authentication

JWT-based auth (Lesson 7), backed by a Redis refresh-token whitelist (Lesson 8):

1. `POST /auth/register` — creates a user (bcrypt-hashed password, unique email/username).
2. `POST /auth/login` — verifies credentials, issues a short-lived **access token** and a
   longer-lived **refresh token** (also stored in Redis for revocation support).
3. Protected routes use `Authorization: Bearer <access_token>` via a `get_current_user`
   dependency (`OAuth2PasswordBearer`).
4. `POST /auth/refresh` — rotates both tokens; rejects tokens not present in the Redis
   whitelist (already-used or revoked tokens fail with `401`).
5. `POST /auth/logout` — removes the refresh token from Redis.
6. Recipe mutation endpoints additionally check **ownership**: acting on someone else's
   recipe returns `403 Forbidden`, not just `401`.

---

## 🧰 Makefile Commands

| Command | Description |
| --- | --- |
| `make build` | Export `requirements.txt` and build the Docker image |
| `make up` | `docker compose up --build -d` — full stack |
| `make down` | Stop and remove containers (volumes preserved) |
| `make reset` | `down` + remove volumes (full data wipe) |
| `make logs` | Tail logs of the `web` service |
| `make migrate` | Run `alembic upgrade head` inside the container |
| `make shell` | Open a bash shell inside the `web` container |
| `make psql` | Open a `psql` shell against the `postgres` container |
| `make export` | Regenerate `requirements.txt` from Poetry |

---

## 🧩 Roadmap / Not Yet Covered

These were out of scope for the homework so far but are natural next steps:

- [ ] Automated tests (unit + integration, e.g. `pytest` + `httpx.AsyncClient`)
- [ ] CI pipeline (lint, type-check, test, build image on push)
- [ ] Rate limiting on auth endpoints
- [ ] Structured logging / request tracing
- [ ] Image uploads for recipes (S3/MinIO)
- [ ] Role-based access control (admin vs regular user)

---

## 📄 License

This is a personal educational project built as coursework. No formal license has been
chosen yet — treat the code as **all rights reserved** unless a `LICENSE` file is added.

---

<p align="center">
  <sub>Built one lesson at a time 🍜 — from an in-memory list to a fully containerized, cached, authenticated API.</sub>
</p>