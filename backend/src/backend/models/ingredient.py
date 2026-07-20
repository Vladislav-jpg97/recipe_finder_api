from sqlalchemy import String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models import Base
from backend.models.mixins import SlugMixin

recipe_ingredients = Table(
    "recipe_ingredients",
    Base.metadata,
    Column(
        "recipe_id",
        Integer,
        ForeignKey("recipes.id",ondelete="CASCADE"),
        primary_key=True
    )
    ,Column(
        "ingredient_id",
        Integer,
        ForeignKey("ingredients.id",ondelete="CASCADE"),
        primary_key=True
    )
)


class Ingredient(SlugMixin,Base):
    __tablename__ = 'ingredients'

    name : Mapped[str] = mapped_column(String(100),unique=True,index=True)

    recipes = relationship("Recipe",secondary=recipe_ingredients,back_populates="ingredients")
