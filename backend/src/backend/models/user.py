from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from backend.models import Base


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    #чтобы время вычислялось прямо в момент создания записи, а не при запуске приложения
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)
