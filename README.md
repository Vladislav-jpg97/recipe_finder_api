# 🍳 Recipe Finder API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License">
</p>

**Recipe Finder API** is a modern asynchronous RESTful web application designed for searching, creating, and managing culinary recipes. The project is built following strict backend development standards: layered architecture (Repository/Service pattern), Pydantic data validation, database migrations with Alembic, JWT authentication, and Redis caching.

---

## 🛠 Tech Stack

* **Core:** Python 3.12, FastAPI, Uvicorn
* **Database & ORM:** PostgreSQL, SQLAlchemy 2.0 (Async), Alembic
* **Validation & Settings:** Pydantic v2, pydantic-settings
* **Caching & Broker:** Redis (asyncio) + Refresh Token Whitelist
* **Security:** python-jose (JWT), passlib (Bcrypt)
* **Infrastructure:** Docker, Docker Compose, Makefile

---

## 📁 Project Architecture

The project is structured according to the principles of layered architecture (Separation of Concerns):

```text
app/
├── api/v1/          # FastAPI routers (domain endpoints: recipes, cuisines, ingredients, reviews, auth)
├── core/            # Application core: settings (config), database, cache, security
├── models/          # SQLAlchemy models (User, Recipe, Cuisine, Ingredient, RecipeReview)
├── repositories/    # Database access layer (Data Access Layer)
├── schemas/         # Pydantic schemas for validation and serialization (including Pagination & Filters)
└── services/        # Business logic layer (Service Layer)
🚀 Quick Start (Docker Compose)
The easiest way to run the entire stack (API, PostgreSQL, Redis, automated migrations) is using Docker Compose.

Clone the repository and configure your environment:

Bash
cp .env.docker.example .env.docker
(Edit connection parameters in .env.docker if necessary)

Launch the project with a single Makefile command:

Bash
make up
The interactive API documentation (Swagger UI) will be available at:

http://localhost:8000/docs

📌 Main Endpoints
🔐 Authentication (/api/v1/auth)
POST /auth/register — Register a new user

POST /auth/login — Authenticate and receive JWT tokens (Access & Refresh)

POST /auth/refresh — Refresh token pair via Redis Whitelist

POST /auth/logout — Invalidate refresh token

GET /auth/me — Profile of the currently authenticated user

🍕 Recipes (/api/v1/recipes)
GET /recipes/ — Retrieve a paginated list of recipes with filtering and ILIKE search support

GET /recipes/top-rated — Top 10 highest-rated recipes

GET /recipes/{recipe_id} — Detailed information for a specific recipe (cached in Redis)

POST /recipes/ — Create a new recipe (JWT required)

PATCH /recipes/{recipe_id} — Partially update a recipe (owner only)

DELETE /recipes/{recipe_id} — Delete a recipe (owner only)

⚙️ Useful Commands (Makefile)
Manage your project using these predefined commands:

make up — Start the entire container stack in the background with rebuilds.

make down — Stop the containers.

make reset — Full environment reset including volume deletion (database wipe).

make logs — Stream backend container logs in real-time.

make migrate — Apply pending Alembic migrations.

make shell — Open a bash shell inside the running backend container.