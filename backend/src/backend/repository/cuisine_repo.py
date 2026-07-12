from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Cuisine


class CuisineRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Cuisine]:
        stmt = select(Cuisine).order_by(Cuisine.name)
        result = await self.session.execute(stmt)
        cuisines = result.scalars().all()
        return cuisines

    async def get_by_id(self, id: int) -> Cuisine:
        stmt = select(Cuisine).where(Cuisine.id == id)
        result = await self.session.execute(stmt)
        cuisine = result.scalar_one_or_none()
        return cuisine

    async def get_by_slug(self, slug: str) -> Cuisine:
        stmt = select(Cuisine).where(Cuisine.slug == slug)
        result = await self.session.execute(stmt)
        cuisine = result.scalar_one_or_none()
        return cuisine

    async def add(self, cuisine: Cuisine) -> Cuisine:
        self.session.add(cuisine)
        await self.session.flush()
        await self.session.refresh(cuisine)
        return cuisine

    async def delete(self, cuisine: Cuisine) -> None:
        await self.session.delete(cuisine)
        await self.session.flush()
