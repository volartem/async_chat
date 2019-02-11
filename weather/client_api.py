import aiohttp
import os


async def get_data(location="kharkiv,ua"):
    # print(ab)
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}".format(location,
                                                                                     os.environ.get('WEATHER_APP_ID',
                                                                                                    ''))
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            return await resp.text()
