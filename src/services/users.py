from src.schemas import UserResponse, UserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from sqlalchemy.future import select

from fastapi.exceptions import HTTPException
from fastapi import status

def hash_password(password: str) -> str:
    return f"#{password}#"

async def create_user(body: UserRequest, session: AsyncSession):
    if await find_user_by_email_and_username(body.email, body.username, session):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exist!")
    
    print("HEllo")
    body_dict = body.model_dump()
    del body_dict["password"]
    user = User(**body_dict, password_hash=hash_password(body.password))
    session.add(user)
    await session.flush()
    return user

async def user_list(session: AsyncSession):
    users = await session.execute(select(User))
    return users.scalars()

async def find_user_by_id(id: str, session: AsyncSession):
    return await session.get(User, id)

async def find_user_by_email(email: str, session: AsyncSession):
    user = await session.execute(select(User).where(User.email == email))
    user = user.scalars().first()
    return user

async def find_user_by_username(username: str, session: AsyncSession):
    user = await session.execute(select(User).where(User.username == username))
    user = user.scalars().first()
    return user
    
async def find_user_by_email_and_username(email, username, session: AsyncSession):
    return await find_user_by_email(email, session) or await find_user_by_username(username, session)


async def update_by_id(id: str, body: UserRequest, session: AsyncSession):
    user = await find_user_by_id(id,session)

    if not user:
        raise HTTPException(status_code=404, detail="No User Found")
    if body.email and await find_user_by_email(body.email, session):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exist")
    if body.username and await find_user_by_username(body.username, session):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username Already Exist")


    if body.email:
        user.email = body.email
    if body.username:
        user.username = body.username
    if body.password:
        user.password_hash = hash_password(body.password)
    if body.is_admin:
        user.is_admin = body.is_admin

    session.add(user)
    await session.flush()
    return user
    