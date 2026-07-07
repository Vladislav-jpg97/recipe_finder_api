import random

from fastapi import APIRouter, Query, HTTPException

from backend.api.v1.enums import SortEnum, CuisineEnum
from backend.schemas.recipes import RecipeBrief, RecipeDetail, RecipeStats
from src.backend.api.v1.db import RECIPES as db_recipes

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@router.get("/", response_model=list[RecipeDetail],description="Список рецептов",summary="Список рецептов")
async def get_recipes(
        cuisine: str | None = None,
        difficulty: str | None = None,
        is_vegetarian: bool | None = None,
        max_time: int | None = None,
        sort_by: SortEnum = SortEnum.rating,
):
    result = db_recipes.copy()

    if cuisine is not None:
        result = [i for i in result if i["cuisine"] == cuisine]

    if difficulty is not None:
        result = [i for i in result if i["difficulty"] == difficulty]

    if is_vegetarian is not None:
        result = [i for i in result if i["is_vegetarian"] == is_vegetarian]

    if max_time is not None:
        result = [i for i in result if i["cooking_time"] <= max_time]

    if sort_by.value == "cooking_time":
        result = sorted(result, key=lambda x: x["cooking_time"])
    else:
        sort_key = "rating" if sort_by.value == "rating" else "calories_per_serving"
        result = sorted(result, key=lambda x: x[sort_key], reverse=True)

    return result


@router.get("/by-ingredients/", response_model=list[RecipeDetail],summary="Поиск по нескольким ингредиентам")
async def get_recipes_by_multiple_ingredients(
        ingredients: list[str] = Query(default=[]),
):
    if not ingredients:
        return []
    result = db_recipes.copy()
    lower = [
        i.lower().strip(" ")
        for i in ingredients
    ]
    matched_recipes = []

    for recipe in result:
        if all(
                any(search_ing in recipe_ing["name"].lower() for recipe_ing in recipe["ingredients"])
                for search_ing in lower
        ):
            matched_recipes.append(recipe)

    return matched_recipes


@router.get("/random", response_model=RecipeDetail,summary="Случайный рецепт")
async def get_random_recipe(
        cuisine: CuisineEnum | None = None,
        is_vegetarian: bool | None = None,
):
    result = db_recipes.copy()

    if cuisine is not None:
        result = [
            res
            for res in result
            if res["cuisine"] == cuisine.value
        ]

    if is_vegetarian is not None:
        result = [
            res
            for res in result
            if res["is_vegetarian"] == is_vegetarian
        ]

    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return random.choice(result)


@router.get("/stats",response_model=RecipeStats,summary="Статистика")
async def get_recipe_stats():
    result = db_recipes.copy()
    if result:
        cuisine_counts = {}
        difficulty_counts = {}

        for res in result:
            name_cuisine = res["cuisine"]
            cuisine_counts[name_cuisine] = cuisine_counts.get(name_cuisine, 0) + 1

            name_difficulty = res["difficulty"]
            difficulty_counts[name_difficulty] = difficulty_counts.get(name_difficulty, 0) + 1

        avg_rating = sum(r["rating"] for r in result) / len(result)

        return {
            "total": len(result),
            "vegetarian_count": len([i for i in result if i["is_vegetarian"]]),
            "by_cuisine": cuisine_counts,
            "by_difficulty": difficulty_counts,
            "average_rating": round(avg_rating, 2),  # Добавили поле по ТЗ
            "fastest_recipe": min(result, key=lambda x: x["cooking_time"])["title"],
            "slowest_recipe": max(result, key=lambda x: x["cooking_time"])["title"]
        }
    return None


@router.get("/by-ingredients/{ingredient}", response_model=list[RecipeDetail],summary="Рецепты по ингредиенту")
async def get_recipes_by_single_ingredient(
        ingredients: str,
):
    if ingredients:
        result = db_recipes.copy()
        lower_ing = ingredients.lower().strip(" ")
        matched_recipes = []

        for recipe in result:
            if any(lower_ing in recipe_ing["name"].lower() for recipe_ing in recipe["ingredients"]):
                matched_recipes.append(recipe)
        return matched_recipes
    return []




@router.get("/{slug}/scale", response_model=list[RecipeDetail],summary="Калькулятор порций")
async def get_recipe_scale(
        slug: str,
        servings: int | None = 1,
):
    result = [
        rec.copy()
        for rec in db_recipes
        if rec["slug"] == slug
    ]

    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")


    for recipe in result:
        recipe["servings"] = servings
        recipe["calories_per_serving"] = recipe["calories_per_serving"] * servings
        recipe["ingredients"] = [
            {"name": ing["name"], "amount": round(ing["amount"] * servings, 2)}
            for ing in recipe["ingredients"]
        ]

    return result


@router.get("/{slug}", response_model=RecipeDetail,description="Один рецепт",summary="Один рецепт")
async def get_recipe_detail(slug: str):
    for rec in db_recipes:
        if rec["slug"] == slug:
            return rec

    raise HTTPException(status_code=404, detail="Recipe not found")

@router.get("/{slug}/similar", response_model=list[RecipeDetail],summary="Похожие рецепты")
async def get_similar_recipes(slug: str):
    get_db = db_recipes.copy()
    current = next(
        (
            i
            for i in get_db
            if i["slug"] == slug
        ),
        None
    )
    if not current:
        raise HTTPException(status_code=404, detail="Recipe not found")
    similar = [
        rec
        for rec in db_recipes
        # Безопасное сравнение:
        if rec["cuisine"].lower() == current["cuisine"].lower() and rec["slug"] != slug
    ]
    return similar[0:3]

