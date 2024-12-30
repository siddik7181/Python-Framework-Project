from pydantic import BaseModel
from typing import Union
from datetime import datetime

class MessageBase(BaseModel):
    message: str

class MessageCreate(MessageBase):
    room_id: str
    author_id: str
    pass

class MessageOut(MessageBase):
    id: str
    room_id: str
    author_id: str

    created_at: datetime
    modified_at: datetime
    
    class Config:
        orm_mode = True

class MessageUpdate(BaseModel):
    message: Union[str, None] = None
        
