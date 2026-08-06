import json
from typing import Any, Annotated

from redis import asyncio as aioredis
from fastapi import Depends
from redis.asyncio import Redis

from backend.core.config import settings


async def get_redis_client() -> Redis:
    return Redis.from_url(
        settings.redis_url,
        encoding = 'utf-8',
        decode_responses = True,
    )

RedisDep = Annotated[
    Redis,
    Depends(get_redis_client),
]

class CacheService:
    def __init__(self, client: Redis):
        self.client = client

    async def get(self, key: str) -> Any | None:
        value = await self.client.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
            self,
            key: str, value: Any, ttl: int = 300
    ) -> None:
        await self.client.setex(key,ttl,json.dumps(value,default=str))

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        keys = await self.client.keys(pattern)
        if keys:
            await self.client.delete(*keys)

    async def close(self) -> None:
        await self.client.aclose()

async def get_cache_service(
        client: Redis,
) -> CacheService:
    return CacheService(client)

CacheServiceDep = Annotated[
    CacheService,
    Depends(get_cache_service),
]

redis_client = aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
cache = CacheService(client=redis_client)


