import sys
import asyncio
import jinja2
import aiohttp_jinja2
from aiohttp import web
from chat.routes import setup_routes
from chat.middleware import setup_middlewares


def init(loop):
    app = web.Application(loop=loop)
    loader = jinja2.PackageLoader('chat', 'templates')
    aiohttp_jinja2.setup(app, loader=loader)
    setup_routes(app)
    setup_middlewares(app)
    return app


def main(argv):
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app,
                host='127.0.0.1',
                port=8080)

if __name__ == '__main__':
    main(argv=sys.argv[1:])


