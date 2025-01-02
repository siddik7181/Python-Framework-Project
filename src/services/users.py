from src.schemas import UserRequest, CommonFilters
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from sqlalchemy import select

from fastapi.exceptions import HTTPException
from fastapi import status

from .common import CommonService

class UserService:

    @classmethod
    def hash_password(cls, password: str) -> str:
        return f"#{password}#"

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.hash_password(plain_password) == hashed_password

    @classmethod
    async def create_user(cls, body: UserRequest, session: AsyncSession):
        if await cls.find_user_by_email_and_username(body.email, body.username, session):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exist!")
        
        body_dict = body.model_dump()
        del body_dict["password"]
        user = User(**body_dict, password_hash = cls.hash_password(body.password))
        session.add(user)
        await session.flush()
        return user

    @classmethod
    async def user_list(cls, filters: CommonFilters, session: AsyncSession):
        return await CommonService.list(User, filters, session)

    @classmethod
    async def find_user_by_id(cls, id: str, session: AsyncSession):
        return await session.get(User, id)

    @classmethod
    async def find_user_by_email(cls, email: str, session: AsyncSession):
        user = await session.execute(select(User).where(User.email == email))
        user = user.scalars().first()
        return user

    @classmethod
    async def find_user_by_username(cls, username: str, session: AsyncSession):
        user = await session.execute(select(User).where(User.username == username))
        user = user.scalars().first()
        return user
        
    @classmethod
    async def find_user_by_email_and_username(cls, email, username, session: AsyncSession):
        return await cls.find_user_by_email(email, session) or await cls.find_user_by_username(username, session)

    @classmethod
    async def authenticate_user(cls, username: str, password: str, session: AsyncSession):
        user = await cls.find_user_by_username(username, session)
        if not user or not cls.verify_password(password, user.password_hash):
            None
        return user

    @classmethod
    async def update_by_id(cls, id: str, body: UserRequest, session: AsyncSession):
        user = await cls.find_user_by_id(id,session)

        if not user:
            raise HTTPException(status_code=404, detail="No User Found")
        if body.email and await cls.find_user_by_email(body.email, session):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email Already Exist")
        if body.username and await cls.find_user_by_username(body.username, session):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username Already Exist")


        if body.email:
            user.email = body.email
        if body.username:
            user.username = body.username
        if body.password:
            user.password_hash = cls.hash_password(body.password)
        if body.is_admin:
            user.is_admin = body.is_admin

        session.add(user)
        await session.flush()
        return user
    