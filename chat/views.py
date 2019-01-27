import aiohttp_jinja2
from .models import get_all_rooms_and_messages


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['models'].acquire() as conn:
        messages, rooms = await get_all_rooms_and_messages(conn)
        return {'messages': messages, 'rooms': rooms}
