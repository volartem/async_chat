import aiohttp
import os


async def get_data(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            return await resp.text()
