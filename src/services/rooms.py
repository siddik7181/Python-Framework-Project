
from src.schemas import RoomCreate
from src.models import Room

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi.exceptions import HTTPException
from fastapi import status

class RoomService:

    @classmethod
    async def create_room(cls, body: RoomCreate, session: AsyncSession):
        if await cls.find_room_by_name(body.name, session):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Choose a different room name!")
        print(body.model_dump())
        room = Room(**body.model_dump())
        session.add(room)
        await session.flush()
        return room

    @classmethod
    async def list_rooms(cls, session: AsyncSession):
        rooms = await session.execute(select(Room))
        return rooms.scalars()

    @classmethod
    async def find_room_by_id(cls, id: str, session: AsyncSession):
        return await session.get(Room, id)

    @classmethod
    async def find_room_by_name(cls, name: str, session: AsyncSession):
        room = await session.execute(select(Room).where(Room.name == name))
        return room.scalars().first()