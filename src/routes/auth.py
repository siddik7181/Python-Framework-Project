from fastapi import APIRouter, Depends, Response, status
from src.schemas import UserLogin, UserResponse

from datetime import timedelta, datetime, timezone

from src.dependencies import get_db
from src.services import UserService

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login/", response_model=UserResponse)
async def login(body: UserLogin,response: Response, session: AsyncSession = Depends(get_db)):
    user = await UserService.login_user(body, session)
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    response.set_cookie(
        key="session_id", 
        value=user.id, 
        max_age=timedelta(minutes=30),
        expires=expires,
        secure=True, 
        httponly=True
    )
    return user

@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="session_id")
    response.set_cookie(key="session_id", value="", expires=0) 
