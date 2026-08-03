import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.cache import cache
from backend.core.cache_keys import CacheKeys
from backend.models import Cuisine
from backend.schemas.cuisines import CuisineRead


class CuisineRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Cuisine]:
        cache_key = CacheKeys.cuisine_list()
        cache_data = cache.get(cache_key)
        if cache_data:
            return json.loads(cache_data) if isinstance(cache_data, str) else cache_data

        stmt = select(Cuisine).order_by(Cuisine.name)
        result = await self.session.execute(stmt)
        cuisines = result.scalars().all()
        serialized_data = [
            CuisineRead.model_validate(c).model_dump(mode="json")
            for c in cuisines
        ]
        cache.set(cache_key, json.dumps(serialized_data), ttl=3600)

        return serialized_data

    async def get_by_id(self, cuisine_id: int) -> Cuisine:
        stmt = select(Cuisine).where(Cuisine.id == cuisine_id)
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
