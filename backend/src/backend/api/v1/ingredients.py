from fastapi import APIRouter
from starlette import status

from backend.dependencies.ingredients import IngredientServiceDep

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
)

@router.get("/", status_code=status.HTTP_200_OK,summary="Список ингредиентов")
async def get_all_ingredients(
        service: IngredientServiceDep
):
    return await service.get_all()

@router.post("/", status_code=status.HTTP_201_CREATED,summary="Создание ингредиентов")
async def create_ingredient(
        service: IngredientServiceDep,
        name: str,
):
    return await service.create(name)

@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Удаление ингредиентов")
async def delete_ingredient(
        ingredient_id: int,
        service: IngredientServiceDep
):
    return await service.delete(ingredient_id)

