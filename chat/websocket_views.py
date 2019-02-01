import logging

import aiohttp
from aiohttp_security import authorized_userid
from aiohttp import web
from .models import get_room_by_id, create_message

log = logging.getLogger(__name__)


async def websocket_handler(request):
    ws_current = web.WebSocketResponse()
    try:
        room_id = int(request.match_info.get('room'))
        token = request.rel_url.query.get('token')
        async with request.app['models'].acquire() as conn:
            room = await get_room_by_id(conn, room_id)
            user = await authorized_userid(request)

            if not room:
                raise web.HTTPBadRequest

            await ws_current.prepare(request)

            if room_id not in request.app['websockets']:
                request.app['websockets'][room_id] = {}

            if not token:
                await ws_current.send_json({'action': 'error', 'text': "need token"})
                await ws_current.close()
                return ws_current
            else:
                request.app['websockets'][room_id][token] = ws_current
                log.info(' %s joined.', token)
                while True:
                    msg = await ws_current.receive()
                    if msg.type == aiohttp.WSMsgType.text:
                        if user:
                            message = await create_message(conn, msg.data, user['id'], room_id)
                        else:
                            await ws_current.send_json(
                                {'action': 'error', 'username': user, 'text': "need auth"})
                        for ws in request.app['websockets'][room_id].values():
                            if user:
                                await ws.send_json(
                                    {'action': 'sent', 'username': user, 'text': message['message'],
                                     'created': message['created']})
                    else:
                        break

                ws_current = await disconnect(request, ws_current, room_id, token)
                return ws_current
    except ValueError:
        log.exception(":::: Someone try hack ::::")
        return ws_current


async def disconnect(request, ws_current, room_id, token):
    del request.app['websockets'][room_id][token]
    log.info(' %s disconnected.', token)

    await ws_current.close()
    return ws_current
