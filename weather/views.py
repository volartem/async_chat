from aiohttp import web
from weather.client_api import get_data


async def weather_data(request):
    location = request.rel_url.query.get('location')
    data = await get_data(location) if location else await get_data()
    return web.json_response(data)
