from pydantic import BaseModel

# Это необходимо добавить, чтобы описать новую структуру ингредиента
class RecipeIngredient(BaseModel):
    name: str
    amount: float  # float, так как у нас есть 0.5 яйца и 0.3 авокадо

class RecipeBrief(BaseModel):
    id: int
    title: str
    slug: str
    cuisine: str
    difficulty: str
    cooking_time: int
    is_vegetarian: bool
    rating: float

class RecipeDetail(RecipeBrief):
    servings: int
    calories_per_serving: int
    ingredients: list[RecipeIngredient]  # Изменили str на модель RecipeIngredient

class RecipeStats(BaseModel):
    total: int
    by_cuisine: dict[str, int]
    by_difficulty: dict[str, int]
    vegetarian_count: int
    average_rating: float
    fastest_recipe: str
    slowest_recipe: str