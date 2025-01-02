from src.schemas import MessageCreate, MessageUpdate
from src.models import Message

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi.exceptions import HTTPException
from fastapi import status

from .users import UserService

class MessageService:

    @classmethod
    async def send_message(cls, message: MessageCreate, session: AsyncSession):
        new_msg = Message(**message.model_dump())
        session.add(new_msg)
        await session.flush()
        return new_msg

    @classmethod
    async def list_messages_by_room(cls, room_id: str, session: AsyncSession):
        stmt = select(Message).where(Message.room_id == room_id)
        messages = await session.execute(stmt)
        return messages.scalars()

    @classmethod
    async def get_message_by_id(cls, id: str, session: AsyncSession):
        return await session.get(Message, id)

    @classmethod
    async def update_message_by_id(cls, id: str, body: MessageUpdate, session: AsyncSession):
        msg = await cls.get_message_by_id(id, session)
        if not msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message Not Found")
        if body.message:
            msg.message = body.message
        session.add(msg)
        await session.flush()
        return msg
    
    @classmethod
    async def find_by_msg_id_and_del_by_super_user(cls, message_id: str, user_id: str, session: AsyncSession):
        
        message = await cls.get_message_by_id(message_id, session)
        if not message:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No content found!")
        
        user = await UserService.find_user_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no User Found")
        

        if message.author_id != user_id and user.is_admin == False: # give this access to only message author & admin..
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized!")
        
        await session.delete(message)
        await session.flush()

        