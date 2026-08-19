
from datetime import datetime

from uuid import UUID, uuid4

from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.core.db import Base

class InboxModel(Base):
    __tablename__ = "inbox"

    event_id: Mapped[UUID] = mapped_column(primary_key=True, unique= True)
    occured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
