from src.models import SessionAsync
from fastapi.exceptions import HTTPException
from fastapi import Request, Depends, Response
from src.services import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserResponse


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


async def get_auth_user(request: Request, session: AsyncSession = Depends(get_db)):
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=401, detail="No Session ID Found")
    
    current_user = await UserService.find_user_by_id(session_id, session)
    if not current_user:
        raise HTTPException(status_code=401, detail="No Valid Session Id Found!!")
    
    # return UserResponse(**current_user.__dict__)
    return UserResponse.model_validate(current_user)


async def only_admin(user: UserResponse = Depends(get_auth_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have admin privileges.")

async def alreday_logged_in(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        raise HTTPException(status_code=400, detail="Already Logged In!!")
    