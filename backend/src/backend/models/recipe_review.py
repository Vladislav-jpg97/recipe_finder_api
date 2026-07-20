from datetime import datetime

from sqlalchemy import ForeignKey, String, TEXT, func, Integer, CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from backend.models import Base


class RecipeReview(Base):
    __tablename__ = 'recipe_reviews'

    recipe_id : Mapped[int] = mapped_column(ForeignKey('recipes.id',ondelete='CASCADE'),)
    author_name : Mapped[str] = mapped_column(String(100))
    rating : Mapped[int] = mapped_column(Integer,CheckConstraint("rating >= 1 AND rating <= 5"),default=0)
    content : Mapped[str] = mapped_column(TEXT , min_length=10)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())