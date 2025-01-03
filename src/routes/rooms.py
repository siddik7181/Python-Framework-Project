
from fastapi import APIRouter, status, Depends
from src.schemas import RoomBase, RoomCreate, RoomResponse, MessageBase, MessageOut, MessageCreate, MessageUpdate, UserResponse, CommonFilters
from src.services import RoomService, MessageService
from typing import List
from src.dependencies import get_db, get_current_user

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/rooms", tags=["rooms"], dependencies=[Depends(get_current_user)])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomResponse)
async def create_room(room: RoomBase, session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    new_room = RoomCreate(**room.model_dump(), owner_id=current_user.id)
    return await RoomService.create_room(new_room, session)

@router.get("/", response_model=List[RoomResponse])
async def get_rooms(filters: CommonFilters, session: AsyncSession = Depends(get_db)):
    return await RoomService.list_rooms(filters, session)

@router.post("/{room_id}/messages/", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
async def send_message(room_id: str, message: MessageBase, session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    new_msg = MessageCreate(**message.model_dump(), room_id=room_id, author_id=current_user.id)
    return await MessageService.send_message(new_msg, session)

@router.get("/{room_id}/messages/", response_model=List[MessageOut])
async def get_messages(room_id: str, filters: CommonFilters, session: AsyncSession = Depends(get_db)):
    return await MessageService.list_messages_by_room(room_id, filters, session)

@router.delete("/{room_id}/messages/{message_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(room_id: str, message_id: str, session: AsyncSession = Depends(get_db), current_user: UserResponse = Depends(get_current_user) ):
    await MessageService.find_by_msg_id_and_del_by_super_user(message_id, current_user.id, session)
    return {"message": f"Message {message_id} deleted from room {room_id}"}

@router.patch("/{room_id}/messages/{message_id}/", response_model=MessageOut)
async def update_message(room_id: str, message_id: str, message: MessageUpdate, session: AsyncSession = Depends(get_db)):
    return await MessageService.update_message_by_id(message_id, message, session)
