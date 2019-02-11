from chat.main import init


async def factory():
    app = await init()
    return app
