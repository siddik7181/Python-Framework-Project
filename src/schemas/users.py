
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr    
    is_admin: bool = False

class UserResponse(UserBase):
    id: str
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True

class UserInDb(UserResponse):
    password_hash: str


class UserRequest(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=50, default=None)
    email: Optional[EmailStr] = Field(default=None)
    is_admin: Optional[bool] =  Field(default=None)
    password: Optional[str] = Field(min_length=8, default=None)


class UserLogin(BaseModel):
    username: str
    password: str = Field(min_length=8)