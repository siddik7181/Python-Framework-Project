
from .users import create_user, find_user_by_id, find_user_by_email, user_list, update_by_id

from .rooms import create_room, list_rooms

from .messages import send_message, list_messages_by_room, update_message_by_id, find_by_msg_id_and_del_by_super_user

class UserService:
    create_user = create_user
    find_user_by_id = find_user_by_id
    find_user_by_email = find_user_by_email
    user_list = user_list
    update_by_id = update_by_id

class RoomService:
    create_room = create_room
    list_rooms = list_rooms


class MessageService:
    send_message = send_message
    list_messages_by_room = list_messages_by_room
    update_message_by_id = update_message_by_id
    find_by_msg_id_and_del_by_super_user = find_by_msg_id_and_del_by_super_user