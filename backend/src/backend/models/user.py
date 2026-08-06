from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    #чтобы время вычислялось прямо в момент создания записи, а не при запуске приложения
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
