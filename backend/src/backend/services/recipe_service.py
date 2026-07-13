import json

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Recipe, Cuisine
from backend.repository.recipe_repo import RecipeRepository
from backend.schemas.recipes import RecipeCreate, RecipeUpdate
from backend.utils.slug import SlugGenerate


class RecipeService:

    def __init__(
            self,
            repo: RecipeRepository,
            session: AsyncSession
    ):
        self.repo = repo
        self.session = session

    async def get_all(self) -> list[Recipe]:
        recipe = await self.repo.get_all()
        return recipe

    async def get_or_404(self,recipe_id: int) -> Recipe:
        recipe = await self.repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe


    async def create(self, recipe: RecipeCreate) -> Recipe:
        base_slug = SlugGenerate.generate(recipe.title)
        slug = base_slug
        counter = 1

        while await self.repo.get_by_slug(slug):
            slug = SlugGenerate.add_suffix(base_slug, counter)
            counter += 1
        cuisine_exists = await self.session.get(Cuisine, recipe.cuisine_id)
        if not cuisine_exists:
            raise HTTPException(
                status_code=400,
                detail=f"Кухня с ID {recipe.cuisine_id} не найдена"
            )

        ingredients_data = [ing.model_dump() for ing in recipe.ingredients]

        new_recipe = Recipe(
            title=recipe.title,
            slug=slug,
            cuisine_id=recipe.cuisine_id,
            difficulty=recipe.difficulty,
            cooking_time=recipe.cooking_time,
            is_vegetarian=recipe.is_vegetarian,
            rating=recipe.rating,
            servings=recipe.servings,
            calories_per_serving=recipe.calories_per_serving,
            ingredients=ingredients_data,
        )

        await self.repo.add(new_recipe)
        await self.session.commit()
        await self.session.refresh(new_recipe)
        return new_recipe

    async def update(self,recipe_id: int,recipe_update: RecipeUpdate) -> Recipe:
        recipe = await self.repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        update_data = recipe_update.model_dump(exclude_unset=True)

        if "title" in update_data:
            new_title = update_data["title"]
            update_data["slug"] = SlugGenerate.generate(new_title)
        for k,v in update_data.items():
            setattr(recipe, k, v)

        await self.session.commit()
        await self.session.refresh(recipe)
        return recipe


    async def delete(self,recipe_id: int) -> None:
        recipe = await self.repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        await self.session.delete(recipe)
        await self.session.commit()
