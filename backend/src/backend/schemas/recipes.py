from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RecipeIngredient(BaseModel):
    name: str
    amount: float


class RecipeBrief(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=200)
    slug: str = Field(min_length=3, max_length=200)
    cuisine: str = Field(min_length=2, max_length=50)
    difficulty: str = Literal["easy", "medium", "hard"]
    cooking_time: int = Field(ge=1, le=600)
    is_vegetarian: bool = Field(default=False)
    rating: float = Field(ge=0, le=5, default=0)


class RecipeDetail(RecipeBrief):
    model_config = ConfigDict(from_attributes=True)
    servings: int = Field(ge=1, le=50)
    calories_per_serving: int = Field(ge=0)
    ingredients: list[RecipeIngredient] = Field(min_length=1, max_length=30)


class RecipeStats(BaseModel):
    total: int
    by_cuisine: dict[str, int]
    by_difficulty: dict[str, int]
    vegetarian_count: int
    average_rating: float
    fastest_recipe: str
    slowest_recipe: str


class RecipeCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    slug: str = Field(min_length=3, max_length=200)
    cuisine_id: int
    difficulty: Literal["easy", "medium", "hard"]
    cooking_time: int = Field(ge=1, le=600)
    servings: int = Field(ge=1, le=50)
    calories_per_serving: int = Field(ge=0)
    ingredients: list[RecipeIngredient]
    is_vegetarian: bool = False
    rating: float = Field(ge=0, le=5, default=0)

    @field_validator('slug', mode="before")
    @classmethod
    def validate_slug(cls, v):
        if isinstance(v, str):
            return v.lower().strip().replace(' ', '-')
        return v


class RecipeUpdate(BaseModel):
    title: str | None = Field(min_length=3, max_length=200)
    cooking_time: int | None = Field(ge=1, le=600)
    is_vegetarian: bool | None = Field(default=False)
    rating: float | None = Field(ge=0, le=5, default=0)
    servings: int | None = Field(ge=1, le=50)
