import aiohttp_jinja2
from .models import get_all_rooms


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['models'].acquire() as conn:
        rooms = await get_all_rooms(conn)
        return {'rooms': rooms}
