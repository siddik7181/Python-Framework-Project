
from fastapi import APIRouter, status, Depends
from src.schemas import RoomBase, RoomResponse
from src.services import RoomService
from typing import List
from src.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomResponse)
async def create_room(room: RoomBase, session: AsyncSession = Depends(get_db)):
    return await RoomService.create_room(room, session)

@router.get("/", response_model=List[RoomResponse])
async def get_rooms(session: AsyncSession = Depends(get_db)):
    return await RoomService.list_rooms(session)

@router.post("/{room_id}/messages/", status_code=status.HTTP_201_CREATED)
async def send_message(room_id: int):
    return {"message": f"Message sent to room {room_id}"}

@router.get("/{room_id}/messages/")
async def get_messages(room_id: int):
    return {"message": f"Messages retrieved from room {room_id}"}

@router.delete("/{room_id}/messages/{message_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(room_id: int, message_id: int):
    return {"message": f"Message {message_id} deleted from room {room_id}"}

@router.patch("/{room_id}/messages/{message_id}/")
async def update_message(room_id: int, message_id: int):
    return {"message": f"Message {message_id} updated in room {room_id}"}

