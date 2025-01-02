from src.models import SessionAsync

from src.utils import  verify_token

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from src.services import UserService
from src.schemas import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    session = SessionAsync()
    try:
        yield session
    except:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = verify_token(token)
    print(payload)
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = await UserService.find_user_by_username(username, db)
    if user is None:
        raise credentials_exception
    return UserResponse.model_validate(user)