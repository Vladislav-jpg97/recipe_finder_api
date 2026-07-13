from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.models import Cuisine
from backend.repository.cuisine_repo import CuisineRepository
from backend.utils.slug import SlugGenerate


class CuisineService:

    def __init__(
            self,
            repo: CuisineRepository,
            session: AsyncSession,
    ):
        self.repo = repo
        self.session = session

    async def get_all(self) -> list[Cuisine]:
        cuisines = await self.repo.get_all()
        return cuisines

    async def get_or_404(self, cuisine_id: int) -> Cuisine:
        cuisine = await self.repo.get_by_id(cuisine_id)

        if not cuisine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuisine not found"
            )
        return cuisine

    async def create(self, name: str, country_code: str) -> Cuisine:
        slug = SlugGenerate.generate(name)
        cuisine = await self.repo.get_by_slug(slug)
        if cuisine:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cuisine with slug '{slug}' already exists"
            )
        new_cuisine = Cuisine(
            name=name,
            slug=slug,
            country_code=country_code,
        )
        await self.repo.add(new_cuisine)
        await self.session.commit()
        await self.session.refresh(new_cuisine)
        return cuisine

    async def delete(self, cuisine_id) -> None:
        cuisine = await self.repo.get_by_id(cuisine_id)
        if not cuisine:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        await self.repo.delete(cuisine)
        await self.session.commit()

