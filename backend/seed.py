import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from backend.models import Recipe, Cuisine
from src.backend.api.v1.db import RECIPES
from backend.core.config import settings

DATABASE_URL = settings.database_url


async def seed_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    Async_Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Async_Session() as session:
        print("--- Подготовка кухонь ---")
        unique_cuisines = {recipe['cuisine'] for recipe in RECIPES}

        for c_name in unique_cuisines:
            res = await session.execute(select(Cuisine).where(Cuisine.name == c_name))
            cuisine = res.scalar()

            if cuisine is None:
                new_cuisine = Cuisine(
                    name=c_name,
                    country_code=c_name[:2].upper(),
                    slug=c_name.lower().replace(" ", "-")
                )
                session.add(new_cuisine)
                try:
                    await session.commit()
                    print(f"Кухня '{c_name}' успешно создана.")
                except Exception:
                    await session.rollback()
                    print(f"Кухня '{c_name}' уже была создана другим процессом, пропускаем.")
            else:
                print(f"Кухня '{c_name}' найдена в БД.")

        # После цикла убедимся, что сессия чиста
        print("Кухни синхронизированы.")

        try:
            await session.commit()
            print("Кухни синхронизированы с базой данных.")
        except Exception as e:
            print(f"Ошибка при сохранении кухонь: {e}")
            await session.rollback()

        print("\n--- Подготовка рецептов ---")
        added_count = 0
        for data in RECIPES:
            try:
                result = await session.execute(
                    select(Recipe).where(Recipe.slug == data["slug"])
                )
                if result.scalar():
                    continue

                res = await session.execute(
                    select(Cuisine).where(Cuisine.name == data["cuisine"])
                )
                cuisine_obj = res.scalar()

                if not cuisine_obj:
                    print(f"!!! ОШИБКА: Кухня '{data['cuisine']}' не найдена.")
                    continue

                new_recipe = Recipe(
                    title=data["title"],
                    slug=data["slug"],
                    cuisine_id=cuisine_obj.id,
                    difficulty=data["difficulty"],
                    cooking_time=data["cooking_time"],
                    servings=data["servings"],
                    calories_per_serving=data["calories_per_serving"],
                    ingredients=data["ingredients"],
                    is_vegetarian=data["is_vegetarian"],
                    rating=data.get("rating", 0.0)
                )
                session.add(new_recipe)
                added_count += 1

            except Exception as e:
                print(f"!!! ОШИБКА при добавлении {data['title']}: {e}")
                await session.rollback()

        await session.commit()
        print(f"\nСкрипт завершен. Добавлено новых рецептов: {added_count}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_db())
