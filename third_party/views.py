import os

from aiohttp import web
from third_party.third_api import get_data


async def weather_data(request):
    # location = request.rel_url.query.get('location')
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric".format("kharkiv,ua",
                                                                                                  os.environ.get(
                                                                                                      'WEATHER_APP_ID',
                                                                                                  ))
    data = await get_data(api_url)
    return web.json_response(data)


async def currency_data(request):
    api_url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    data = await get_data(api_url)
    return web.json_response(data)
