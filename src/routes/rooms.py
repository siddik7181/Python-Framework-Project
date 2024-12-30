
from fastapi import APIRouter, status, Depends, Body
from src.schemas import RoomResponse, MessageBase, MessageOut, MessageCreate, MessageUpdate, UserResponse, RoomCreate
from src.services import RoomService, MessageService
from typing import List
from src.dependencies import get_db, get_auth_user
from sqlalchemy.ext.asyncio import AsyncSession

from typing_extensions import Annotated

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomResponse)
async def create_room(
    room_name: Annotated[str, Body(embed=True)], 
    session: AsyncSession = Depends(get_db), 
    current_user: UserResponse = Depends(get_auth_user)):
    
    body = RoomCreate(name=room_name, owner_id=current_user.id)
    return await RoomService.create_room(body = body, session = session)

@router.get("/", response_model=List[RoomResponse])
async def get_rooms(session: AsyncSession = Depends(get_db)):
    return await RoomService.list_rooms(session = session)

@router.post("/{room_id}/messages/", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
async def send_message(
        room_id: str, 
        body: MessageBase, 
        session: AsyncSession = Depends(get_db), 
        current_user: UserResponse = Depends(get_auth_user)):
    
    new_msg = MessageCreate(message=body.message, author_id=current_user.id, room_id=room_id)
    return await MessageService.send_message(new_msg, session)

@router.get("/{room_id}/messages/", response_model=List[MessageOut])
async def get_messages(
        room_id: str, 
        session: AsyncSession = Depends(get_db)):
    
    return await MessageService.list_messages_by_room(room_id, session)

@router.delete("/{room_id}/messages/{message_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
        room_id: str, 
        message_id: str, 
        current_user: UserResponse = Depends(get_auth_user), 
        session: AsyncSession = Depends(get_db)):
    
    await MessageService.find_by_msg_id_and_del_by_super_user(message_id = message_id, user_id = current_user.id, session = session)
    return {"message": f"Message {message_id} deleted from room {room_id}"}

@router.patch("/{room_id}/messages/{message_id}/", response_model=MessageOut, dependencies=[Depends(get_auth_user)])
async def update_message(
        room_id: str, 
        message_id: str, 
        message: MessageUpdate, 
        session: AsyncSession = Depends(get_db)):
    
    return await MessageService.update_message_by_id(message_id, message, session)
