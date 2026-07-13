from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.core.database import get_db
from backend.repository.cuisine_repo import CuisineRepository
from backend.schemas.cuisines import CuisineRead
from backend.services.cuisine_service import CuisineService

router = APIRouter(prefix="/cuisines", tags=["Cuisine"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Список всех кухонь"
)
async def get_all_cuisines(
        session: AsyncSession = Depends(get_db)
):
    repo = CuisineRepository(session)
    service = CuisineService(repo, session)
    return await service.get_all()


@router.get(
    "/{cuisine_id}",
    status_code=status.HTTP_200_OK,
    summary="Одна кухня"
)
async def get_cuisine(
        cuisine_id: int,
        session: AsyncSession = Depends(get_db)
):
    repo = CuisineRepository(session)
    service = CuisineService(repo, session)
    return await service.get_or_404(cuisine_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать кухню"
)
async def create_cuisine(
        data: CuisineRead,
        session: AsyncSession = Depends(get_db)
):
    repo = CuisineRepository(session)
    service = CuisineService(repo, session)
    return await service.create(data.name, data.country_code)


@router.delete(
    "/{cuisine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить кухню"
)
async def delete_cuisine(
        cuisine_id: int,
        session: AsyncSession = Depends(get_db)
):
    repo = CuisineRepository(session)
    service = CuisineService(repo, session)
    await service.delete(cuisine_id)
    return None
