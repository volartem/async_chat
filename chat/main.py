import sys
import argparse
import asyncio
import jinja2
import aiohttp_jinja2
from envparse import env
from trafaret_config import commandline
from aiohttp import web
from chat.routes import setup_routes
from chat.middleware import setup_middlewares
from chat.utils import TRAFARET
from chat.models import close_pg, init_pg


def init(loop, argv):
    env.read_envfile('../config/.env')
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap,
                                          default_config='../config/chat.yaml')

    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    app = web.Application(loop=loop)
    app['config'] = config

    loader = jinja2.PackageLoader('chat', 'templates')
    aiohttp_jinja2.setup(app, loader=loader)

    # create connection to the database
    app.on_startup.append(init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_middlewares(app)
    return app


def main(argv):
    loop = asyncio.get_event_loop()
    app = init(loop, argv)
    web.run_app(app,
                host='localhost',
                port=8080)

if __name__ == '__main__':
    main(argv=sys.argv[1:])


