from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.models import Ingredient
from backend.repository.ingredient_repo import IngredientRepository
from backend.utils.slug import SlugGenerate


class IngredientService:
    def __init__(self, session: AsyncSession,ingredient_repo: IngredientRepository):
        self.session = session
        self.ingredient_repo = ingredient_repo

    async def create(self,name:str):
        base_slug = SlugGenerate.generate(name)
        slug = base_slug

        existing = await self.ingredient_repo.get_by_slug(slug)

        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ingredient with slug '{slug}' already exists.")

        ingredient = Ingredient(
            name=name,
            slug=slug,
        )
        await self.ingredient_repo.add(ingredient)
        await self.session.commit()
        await self.session.refresh(ingredient)
        return ingredient

    async def delete(self,ingredient_id: int):
        ingredient = await self.ingredient_repo.get_by_id(ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient not found.")
        await self.ingredient_repo.delete(ingredient)
        await self.session.commit()

