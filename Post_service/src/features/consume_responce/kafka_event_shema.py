from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class kafka_event(BaseModel):
    eventID : UUID
    phone : str
    name : str
    status : str
    created_at : datetime
    payload : str