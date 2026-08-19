from datetime import datetime

from uuid import UUID, uuid4
from src.core.db import Base
from sqlalchemy import String, DateTime
from sqlalchemy.orm import  Mapped, mapped_column


class CallbackModel(Base):
    __tablename__ = "callback"

    id: Mapped[UUID] = mapped_column( primary_key=True, default = uuid4())
    phone_number: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(100), default = "new")
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow())



