from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base
from backend.models.mixins import SlugMixin


class Cuisine(SlugMixin, Base):
    __tablename__ = "cuisines"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    country_code: Mapped[str | None] = mapped_column(String(3))
    recipes = relationship("Recipe", back_populates="cuisine")
