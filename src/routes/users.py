
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.schemas import UserResponse, UserRequest, UserUpdate
from typing import List
from src.dependencies import get_db, get_requesting_user
from src.services import UserService

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(body: UserRequest, session: AsyncSession = Depends(get_db)):
    return await UserService.create_user(body, session)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(user_id: str, session: AsyncSession = Depends(get_db)):
    return await UserService.find_user_by_id(user_id, session)

@router.get("/", response_model=List[UserResponse])
async def read_users(session: AsyncSession = Depends(get_db), requesting_user: UserResponse = Depends(get_requesting_user)):
    if not requesting_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to list all users")
    return await UserService.user_list(session)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, body: UserUpdate, session: AsyncSession = Depends(get_db), requesting_user: UserResponse = Depends(get_requesting_user)):
    if requesting_user.id != user_id and not requesting_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update other users")
    return await UserService.update_by_id(user_id, body, session)