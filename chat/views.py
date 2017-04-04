import aiohttp_jinja2
from .models import message


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['models'].acquire() as conn:
        cursor = await conn.execute(message.select())
        records = await cursor.fetchall()
        messages = [dict(q) for q in records]
        return {'messages': messages}
