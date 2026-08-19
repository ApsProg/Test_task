from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CallbackRequest(BaseModel):
    phone: str = Field(min_length=6, max_length=20)
    name: str  = Field(min_length=6, max_length=100)
    source : str = Field(min_length=6, max_length=100)
    comment : str = Field(min_length=6, max_length=100)

class CallbackResponse(BaseModel):
    id : UUID
    phone : str
    name : str
    status : str
    created_at : datetime
