from src.models import SessionAsync
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.services import UserService


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

security = HTTPBasic()
async def get_requesting_user(credentials: HTTPBasicCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    user = await UserService.find_user_by_username(credentials.username, db)
    if not user or not UserService.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user