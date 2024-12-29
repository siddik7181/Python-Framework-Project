
from pydantic import BaseModel, Field
from datetime import datetime

class RoomBase(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    owner_id: str

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: str
    
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True 
