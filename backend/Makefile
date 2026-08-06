export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

up:
	docker compose --env-file .env.docker up --build -d

down:
	docker compose --env-file .env.docker down

reset:
	docker compose --env-file .env.docker down -v

logs:
	docker compose --env-file .env.docker logs -f web

migrate:
	docker compose --env-file .env.docker run --rm migrate

shell:
	docker compose --env-file .env.docker exec web bash

psql:
	docker compose --env-file .env.docker exec postgres psql -U postgres -d recipe_finder

build:
	docker build -t recipe-api:latest .

run:
	docker run --rm -d --name recipe-app --env-file .env.docker -p 8000:8000 recipe-api:latest

stop:
	docker stop recipe-app && docker rm recipe-app

dev:
	poetry run uvicorn backend.main:app --app-dir src --reload