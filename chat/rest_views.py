from aiohttp import web
from .models import get_message_by_id, get_messages_with_users_by_room_id
import uuid
from aiohttp_security import authorized_userid


async def messages_id(request):
    mess_id = int(request.match_info.get('id', 2))
    async with request.app['models'].acquire() as conn:
        record = await get_message_by_id(conn, mess_id)
    return web.json_response(record)


async def messages_room_id(request):
    try:
        room_id = int(request.match_info.get('id', 1))
        async with request.app['models'].acquire() as conn:
            record = await get_messages_with_users_by_room_id(conn, room_id)
        return web.json_response(record)
    except ValueError:
        raise web.HTTPBadRequest


async def generate_uuid(request):
    user = await authorized_userid(request)
    token = "{0}-{1}".format(user['username'].replace(" ", "") if user else str(user), str(uuid.uuid4()))
    return web.json_response({'token': token})
