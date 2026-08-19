from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class CallbackRequested(BaseModel):
    evet_type : str = "callback_requested.v1"
    callback_id : UUID
    phone: str
    occurred_at : datetime