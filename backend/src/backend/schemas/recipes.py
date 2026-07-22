from typing import Literal

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator


class RecipeIngredient(BaseModel):
    name: str
    amount: float


class RecipeBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str = Field(min_length=3, max_length=200)
    slug: str = Field(min_length=3, max_length=200)
    cuisine: str  # Можно оставить str, если добавить поле/свойство или валидатор
    difficulty: Literal["easy", "medium", "hard"]
    cooking_time: int = Field(ge=1, le=600)
    is_vegetarian: bool = Field(default=False)
    rating: float = Field(ge=0, le=5, default=0)

    @field_validator('cuisine', mode="before")
    @classmethod
    def extract_cuisine_name(cls, v):
        # Если пришел объект модели Cuisine, берем его атрибут name
        if hasattr(v, "name"):
            return v.name
        return v


class RecipeDetail(RecipeBrief):
    servings: int = Field(ge=1, le=50)
    calories_per_serving: int = Field(ge=0)
    ingredients: list[RecipeIngredient] = Field(default_factory=list)


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

class RecipeFilters:
    def __init__(
            self,
            search : str | None = None,
            cuisine_id :int | None = None,
            is_vegetarian : bool | None = None,
            difficulty : str | None = None,
            max_cooking_time : int | None = None,
            sort_by : str = Query(
                "created_at" ,
                enum=["created_at", "rating", "cooking_time"]
            ),
            sort_order : str = Query(
                "desc",
                enum=["desc","asc"]
            ),
    ):
        self.search = search
        self.cuisine_id = cuisine_id
        self.is_vegetarian = is_vegetarian
        self.difficulty = difficulty
        self.max_cooking_time = max_cooking_time
        self.sort_by = sort_by
        self.sort_order = sort_order

