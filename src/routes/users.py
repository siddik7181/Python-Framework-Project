
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.schemas import UserResponse, UserRequest, UserUpdate,CommonFilters
from typing import List
from src.dependencies import get_db, get_current_user
from src.services import UserService

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(body: UserRequest, session: AsyncSession = Depends(get_db)):
    return await UserService.create_user(body, session)

@router.get("/", response_model=UserResponse)
async def read_user_by_id(current_user: UserResponse = Depends(get_current_user)):
    return current_user

@router.get("/list", response_model=List[UserResponse])
async def read_users(fillters: CommonFilters, session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to access this")
    return await UserService.user_list(fillters, session)

@router.patch("/", response_model=UserResponse)
async def update_user(body: UserUpdate, session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return await UserService.update_by_id(current_user.id, body, session)