
export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

build:
	export
	docker build -t recipe-api:latest .

run:
	docker run --rm -d --name recipe-app --env-file .env.docker -p 8000:8000 recipe-api:latest

stop:
	docker stop recipe-app && docker rm recipe-app

logs:
	docker logs -f recipe-app

shell:
	docker exec -it recipe-app bash
dev:
	poetry run uvicorn backend.main:app --app-dir src --reload

migrate:
	poetry run alembic upgrade head