
from fastapi import APIRouter, status, Depends
from src.schemas import UserResponse, UserRequest, UserUpdate
from typing import List
from src.dependencies import get_db, get_auth_user, only_admin, alreday_logged_in
from src.services import UserService

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse, dependencies=[Depends(alreday_logged_in)])
async def create_user(body: UserRequest, session: AsyncSession = Depends(get_db)):
    return await UserService.create_user(body, session)

@router.get("/", response_model=UserResponse)
async def read_user(session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_auth_user)):
    return current_user

@router.get("/list", response_model=List[UserResponse], dependencies=[Depends(only_admin)])
async def read_users(session: AsyncSession = Depends(get_db)):
    return await UserService.user_list(session)

@router.patch("/", response_model=UserResponse)
async def update_user(body: UserUpdate, session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_auth_user)):
    return await UserService.update_by_id(current_user.id, body, session)