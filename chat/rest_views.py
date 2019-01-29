from aiohttp import web
from .models import get_message_by_id, get_messages_with_users_by_room_id


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
