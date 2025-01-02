
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

@router.get("/", response_model=UserResponse)
async def read_current_user(current_user: UserResponse = Depends(get_requesting_user), session: AsyncSession = Depends(get_db)):
    return await UserService.find_user_by_id(current_user.id, session)

@router.get("/list", response_model=List[UserResponse])
async def read_users(session: AsyncSession = Depends(get_db), requesting_user: UserResponse = Depends(get_requesting_user)):
    if not requesting_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to list all users")
    return await UserService.user_list(session)

@router.patch("/", response_model=UserResponse)
async def update_user(body: UserUpdate, session: AsyncSession = Depends(get_db), requesting_user: UserResponse = Depends(get_requesting_user)):
    return await UserService.update_by_id(requesting_user.id, body, session)