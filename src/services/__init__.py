
from .users import create_user, find_user_by_id, find_user_by_email, user_list, update_by_id

class UserService:
    create_user = create_user
    find_user_by_id = find_user_by_id
    find_user_by_email = find_user_by_email
    user_list = user_list
    update_by_id = update_by_id