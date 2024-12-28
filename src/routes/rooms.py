
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room():
    return {"message": "Room created successfully"}

@router.get("/")
async def get_rooms():
    return {"message": "Rooms retrieved successfully"}

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

