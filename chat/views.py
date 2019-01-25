import aiohttp_jinja2
from .models import message, room


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['models'].acquire() as conn:
        cursor = await conn.execute(message.select())
        records = await cursor.fetchall()
        cursor_room = await conn.execute(room.select())
        records_room = await cursor_room.fetchall()
        messages = [dict(q) for q in records]
        rooms = [dict(r) for r in records_room]
        return {'messages': messages, 'rooms': rooms}
