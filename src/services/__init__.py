
from .users import create_user, find_user_by_id, find_user_by_email, user_list, update_by_id

from .rooms import create_room, list_rooms

class UserService:
    create_user = create_user
    find_user_by_id = find_user_by_id
    find_user_by_email = find_user_by_email
    user_list = user_list
    update_by_id = update_by_id

class RoomService:
    create_room = create_room
    list_rooms = list_rooms