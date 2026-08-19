from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

class outbox_product(BaseModel):
    event_id : UUID
    occued_at: datetime
    event : str
    payload: str

