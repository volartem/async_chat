import sys
from chat.main import init


async def factory():
    app = await init(sys.argv[1:])
    return app
