from datetime import datetime

from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.core.db import Base


class OutboxModel(Base):
    __tablename__ = "outbox"

    event_id: Mapped[UUID] = mapped_column(primary_key = True, default = uuid4)
    event: Mapped[str] = mapped_column(String(50))
    name : Mapped[str] = mapped_column(String(100))
    phone_number : Mapped[str] = mapped_column(String(100))
    source : Mapped[str] = mapped_column(String(100))
    comment : Mapped[str] = mapped_column(String(100))