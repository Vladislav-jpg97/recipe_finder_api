from backend.models.models import Recipe
from backend.models.cuisine import Cuisine
from backend.models.ingredient import Ingredient, recipe_ingredients
from backend.models.recipe_review import RecipeReview
from backend.models.user import User

# Импортируем Base в самом конце, когда все модели уже зарегистрировались
from backend.models.base import Base

__all__ = ["Base", "Recipe", "Cuisine", "Ingredient", "RecipeReview", "recipe_ingredients", "User"]