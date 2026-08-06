# 🍳 Recipe Finder API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Status-Educational_Project-orange?style=for-the-badge" alt="Status">
</p>

**Recipe Finder API** is an advanced educational coursework project developed to demonstrate professional backend engineering skills. It is an asynchronous RESTful web application designed for searching, creating, and managing culinary recipes, featuring clean layered architecture, robust validation, database migrations, JWT security, and Redis caching.

---

## 🛠 Tech Stack

| Category | Technology / Tool | Purpose |
| :--- | :--- | :--- |
| **Core** | Python 3.12, FastAPI, Uvicorn | High-performance asynchronous web framework |
| **Database** | PostgreSQL 16, SQLAlchemy 2.0 (Async), Alembic | Relational database, asynchronous ORM, and schema migrations |
| **Validation** | Pydantic v2, pydantic-settings | Data validation, serialization, and settings management |
| **Caching** | Redis 7 (asyncio) | Response caching & Refresh Token Whitelist management |
| **Security** | python-jose, passlib (Bcrypt) | JWT authentication and password hashing |
| **DevOps** | Docker, Docker Compose, Makefile | Containerization and workflow automation |

---

## 📁 Project Architecture

The project follows a strict layered architecture (Separation of Concerns) to ensure scalability and maintainability:

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
Explore the interactive API documentation (Swagger UI):

http://localhost:8000/docs

📌 Main Endpoints
🔐 Authentication (/api/v1/auth)
Method	Endpoint	Description	Auth Required
POST	/auth/register	Register a new user	No
POST	/auth/login	Authenticate and receive JWT tokens (Access & Refresh)	No
POST	/auth/refresh	Refresh token pair via Redis Whitelist	No
POST	/auth/logout	Invalidate refresh token	Yes
GET	/auth/me	Profile of the currently authenticated user	Yes
🍕 Recipes (/api/v1/recipes)
Method	Endpoint	Description	Auth Required
GET	/recipes/	Retrieve a paginated list of recipes with filtering & ILIKE search	No
GET	/recipes/top-rated	Retrieve top 10 highest-rated recipes	No
GET	/recipes/{recipe_id}	Detailed information for a specific recipe (cached in Redis)	No
POST	/recipes/	Create a new recipe	Yes
PATCH	/recipes/{recipe_id}	Partially update a recipe (owner only)	Yes
DELETE	/recipes/{recipe_id}	Delete a recipe (owner only)	Yes
⚙️ Useful Commands (Makefile)
Command	Action
make up	Start the entire container stack in the background with rebuilds
make down	Stop the running containers
make reset	Full environment reset including volume and database deletion
make logs	Stream backend container logs in real-time
make migrate	Apply pending Alembic database migrations
make shell	Open a bash shell inside the running backend container