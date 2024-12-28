
from src.schemas import RoomBase
from src.models import Room

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi.exceptions import HTTPException
from fastapi import status

async def create_room(body: RoomBase, session: AsyncSession):
    if await find_room_by_name(body.name, session):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Choose a different room name!")
    
    room = Room(**body.model_dump())
    session.add(room)
    await session.flush()
    return room

async def list_rooms(session: AsyncSession):
    rooms = await session.execute(select(Room))
    return rooms.scalars()

async def find_room_by_id(id: str, session: AsyncSession):
    return await session.get(Room, id)

async def find_room_by_name(name: str, session: AsyncSession):
    room = await session.execute(select(Room).where(Room.name == name))
    return room.scalars().first()