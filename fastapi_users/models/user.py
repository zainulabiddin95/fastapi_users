from datetime import datetime

from sqlalchemy import Integer, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, BYTEA
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )

    username: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    hashed_password: Mapped[bytes] = mapped_column(BYTEA, nullable=False)
