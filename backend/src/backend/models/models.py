from datetime import datetime
from sqlalchemy import JSON, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.ingredient import recipe_ingredients
from backend.models.mixins import SlugMixin


class Recipe(SlugMixin,Base):
    __tablename__ = "recipes"

    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True)
    difficulty: Mapped[str] = mapped_column(String(10))
    cooking_time: Mapped[int]
    servings: Mapped[int]
    calories_per_serving: Mapped[int]
    is_vegetarian: Mapped[bool] = mapped_column(default=False)
    rating: Mapped[float] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    cuisine_id: Mapped[int] = mapped_column(ForeignKey("cuisines.id", ondelete="SET NULL"))
    author_id : Mapped[int] = mapped_column(ForeignKey("authors.id"),nullable=False)

    ingredients = relationship(
        "Ingredient",
        secondary=recipe_ingredients,
        back_populates="recipes",
    )
    cuisine = relationship("Cuisine", back_populates="recipes")

