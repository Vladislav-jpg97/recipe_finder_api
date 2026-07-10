from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from backend.api.v1.enums import SortEnum, CuisineEnum
from backend.schemas.recipes import RecipeDetail, RecipeStats, RecipeCreate, RecipeUpdate
from backend.models.models import Recipe
from backend.core.database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])


# 1. Список рецептов
@router.get("/", response_model=list[RecipeDetail])
async def get_recipes(
        cuisine: str | None = None,
        difficulty: str | None = None,
        is_vegetarian: bool | None = None,
        max_time: int | None = None,
        sort_by: SortEnum = SortEnum.rating,
        db: AsyncSession = Depends(get_db)
):
    query = select(Recipe)
    if cuisine:
        query = query.where(Recipe.cuisine == cuisine)
    if difficulty:
        query = query.where(Recipe.difficulty == difficulty)
    if is_vegetarian is not None:
        query = query.where(Recipe.is_vegetarian == is_vegetarian)
    if max_time:
        query = query.where(Recipe.cooking_time <= max_time)

    if sort_by == SortEnum.cooking_time:
        query = query.order_by(Recipe.cooking_time)
    else:
        sort_col = Recipe.rating if sort_by == SortEnum.rating else Recipe.calories_per_serving
        query = query.order_by(sort_col.desc())
    result = await db.execute(query)
    return result.scalars().all()


# 2. Поиск по нескольким ингредиентам
@router.get("/by-ingredients/", response_model=list[RecipeDetail])
async def get_recipes_by_multiple_ingredients(
        ingredients: list[str] = Query(default=[]),
        db: AsyncSession = Depends(get_db)):
    if not ingredients:
        return []
    query = select(Recipe)
    for ing in ingredients:
        query = query.where(Recipe.ingredients.any(name=ing))
    result = await db.execute(query)
    return result.scalars().all()


# 3. Случайный рецепт
@router.get(
    "/random",
    response_model=RecipeDetail
)
async def get_random_recipe(
        cuisine: CuisineEnum | None = None,
        is_vegetarian: bool | None = None,
        db: AsyncSession = Depends(get_db)
):
    query = select(Recipe)
    if cuisine:
        query = query.where(Recipe.cuisine == cuisine)
    if is_vegetarian is not None:
        query = query.where(Recipe.is_vegetarian == is_vegetarian)

    result = await db.execute(query)
    return result.scalars().all()


# 4. Статистика
@router.get("/stats", response_model=RecipeStats, summary="Статистика")
async def get_recipe_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Recipe))
    recipes = result.scalars().all()

    if recipes:
        cuisine_counts = {}
        difficulty_counts = {}

        for res in recipes:
            name_cuisine = res.cuisine
            cuisine_counts[name_cuisine] = cuisine_counts.get(name_cuisine, 0) + 1

            name_difficulty = res.difficulty
            difficulty_counts[name_difficulty] = difficulty_counts.get(name_difficulty, 0) + 1

        avg_rating = sum(r.rating for r in recipes) / len(recipes)

        return {
            "total": len(recipes),
            "vegetarian_count": len([i for i in recipes if i.is_vegetarian]),
            "by_cuisine": cuisine_counts,
            "by_difficulty": difficulty_counts,
            "average_rating": round(avg_rating, 2),
            "fastest_recipe": min(recipes, key=lambda x: x.cooking_time).title,
            "slowest_recipe": max(recipes, key=lambda x: x.cooking_time).title
        }
    return None


# 5. Создание рецепта
@router.post(
    "/",
    response_model=RecipeDetail)
async def create_recipe(
        data: RecipeCreate,
        db: AsyncSession = Depends(get_db)
):

    ingredients_json = json.dumps(data.ingredients)


    new_recipe = Recipe(
        **data.model_dump(exclude={"ingredients"}),
        ingredients=ingredients_json
    )

    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)

    return new_recipe


# 6. Поиск по одному ингредиенту
@router.get(
    "/by-ingredients/{ingredient}",
    response_model=list[RecipeDetail]
)
async def get_recipes_by_single_ingredient(
        ingredient: str,
        db: AsyncSession = Depends(get_db)
):
    query = select(Recipe).where(Recipe.ingredients.any(name=ingredient))
    result = await db.execute(query)
    return result.scalars().all()


# 7. Калькулятор порций
@router.get(
    "/{slug}/scale",
    response_model=list[RecipeDetail],
    summary="Калькулятор порций"
)
async def get_recipe_scale(
        slug: str,
        servings: int | None = 1,
        db: AsyncSession = Depends(get_db)
):

    result = await db.execute(select(Recipe).where(Recipe.slug == slug))
    recipe = result.scalar_one_or_none()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    recipe_dict = recipe.__dict__.copy()

    recipe_dict["servings"] = servings
    recipe_dict["calories_per_serving"] = recipe.calories_per_serving * servings

    recipe_dict["ingredients"] = [
        {
            "name": ing["name"],
            "amount": round(ing["amount"] * servings, 2)
        }
        for ing in recipe.ingredients
    ]

    return [recipe_dict]


# 8. Один рецепт
@router.get(
    "/{slug}",
    response_model=RecipeDetail)
async def get_recipe_by_slug(
        slug: str,
        db: AsyncSession = Depends(get_db)
):
    query = select(Recipe).where(Recipe.slug == slug)
    result = await db.execute(query)
    recipe = result.scalar_one_or_none()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found")

    return recipe


# 9. Похожие рецепты
@router.get(
    "/{slug}/similar",
    response_model=list[RecipeDetail]
)
async def get_similar_recipes(
        slug: str,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Recipe).where(Recipe.slug == slug))
    current = result.scalar_one_or_none()
    if not current: raise HTTPException(status_code=404, detail="Recipe not found")
    res = await db.execute(select(Recipe).where(Recipe.cuisine == current.cuisine, Recipe.slug != slug).limit(3))
    return res.scalars().all()


# 10. Обновление рецепта
@router.patch(
    "/{slug}",
    response_model=RecipeDetail
)
async def update_recipe(
        slug: str,
        data: RecipeUpdate,
        db: AsyncSession = Depends(get_db)
):
    query = select(Recipe).where(Recipe.slug == slug)
    result = await db.execute(query)
    recipe = result.scalar_one_or_none()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "ingredients":
            value = json.dumps(value)
        setattr(recipe, key, value)

    await db.commit()
    await db.refresh(recipe)

    return recipe
