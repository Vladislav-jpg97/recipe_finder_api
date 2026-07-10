import asyncio
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session

from backend.models import Recipe
from src.backend.api.v1.db import RECIPES

from backend.core.config import settings_seed

DATABASE_URL = settings_seed.database_url

async def seed_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    Async_Session = async_sessionmaker(engine, expire_on_commit=False)

    recipes_data = RECIPES
    added_count = 0

    async with Async_Session() as AsyncSession:
        for data in recipes_data:
            result = await AsyncSession.execute(
                select(Recipe).where(Recipe.slug == data["slug"])
            )
            existing = result.scalar()
            if not existing:
                new_recipe = Recipe(
                    title=data["title"],
                    slug=data["slug"],
                    cuisine=data["cuisine"],
                    difficulty=data["difficulty"],
                    cooking_time=data["cooking_time"],
                    servings=data["servings"],
                    calories_per_serving=data["calories_per_serving"],
                    ingredients=data["ingredients"],
                    is_vegetarian=data["is_vegetarian"],
                )
                AsyncSession.add(new_recipe)
                added_count += 1
                print(f"Добавлен рецепт: {data['title']}")
            else:
                print(f"Рецепт '{data['slug']}' уже существует, пропускаем.")
        await AsyncSession.commit()
        print(f"\nСкрипт завершен. Всего добавлено новых рецептов: {added_count}")

        # Закрываем соединение
    await engine.dispose()
if __name__ == "__main__":
    asyncio.run(seed_db())

