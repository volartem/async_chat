from .models import get_user_by_username
from .security import check_password_hash


async def validate_login_form(conn, form):
    username = form['username']
    password = form['password']

    if not username:
        return 'username is required'
    if not password:
        return 'password is required'

    user = await get_user_by_username(conn, username)

    if not user:
        return 'Invalid username'
    if not check_password_hash(password, user['password']):
        return 'Invalid password'
    else:
        return None
