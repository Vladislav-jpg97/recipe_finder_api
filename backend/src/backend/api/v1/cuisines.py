from fastapi import APIRouter
from starlette import status
from backend.dependencies.cuisines import CuisineServiceDep
from backend.schemas.cuisines import CuisineCreate

router = APIRouter(prefix="/cuisines", tags=["Cuisine"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Список всех кухонь"
)
async def get_all_cuisines(
        service: CuisineServiceDep,
):
    return await service.get_all()


@router.get(
    "/{cuisine_id}",
    status_code=status.HTTP_200_OK,
    summary="Одна кухня"
)
async def get_cuisine(
        cuisine_id: int,
        service: CuisineServiceDep
):
    return await service.get_or_404(cuisine_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать кухню"
)
async def create_cuisine(
        data: CuisineCreate,
        service: CuisineServiceDep
):
    return await service.create(data.name, data.country_code)


@router.delete(
    "/{cuisine_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить кухню"
)
async def delete_cuisine(
        cuisine_id: int,
        service: CuisineServiceDep
):
    await service.delete(cuisine_id)
    return None
