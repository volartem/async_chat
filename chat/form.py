from .models import get_user_by_username
from .security import check_password_hash
import re


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


async def validate_signup_form(conn, form):
    username = form['username']
    password = form['password']
    password_confirm = form['password-confirm']
    email = form['email']

    if not email:
        return 'email is required'
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return 'email is not correct'
    if not username:
        return 'username is required'
    if not password:
        return 'password is required'
    if password != password_confirm:
        return 'you enter not equals passwords'

    user = await get_user_by_username(conn, username)

    if user:
        return 'User with username {} already exists. Try another username.'.format(username)
    else:
        return None
