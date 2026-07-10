from datetime import datetime
from sqlalchemy import JSON, func, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(220), unique=True, index=True)
    cuisine: Mapped[str] = mapped_column(String(50), index=True)
    difficulty: Mapped[str] = mapped_column(String(10))
    cooking_time: Mapped[int]
    servings: Mapped[int]
    calories_per_serving: Mapped[int]
    ingredients: Mapped[dict] = mapped_column(JSON, default=dict)
    is_vegetarian: Mapped[bool] = mapped_column(default=False)
    rating: Mapped[float] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
