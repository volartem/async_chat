import sys
import argparse
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import authorized_userid
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy
from chat.db_auth import DBAuthorizationPolicy
import aioredis
import jinja2
import aiohttp_jinja2
from envparse import env
from trafaret_config import commandline
from aiohttp import web
from chat.routes import setup_routes
from chat.middleware import setup_middlewares
from chat.utils import TRAFARET
from chat.models import close_pg, init_pg
import logging


async def init(argv):
    env.read_envfile('.env')
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap,
                                          default_config='../config/chat.yaml')

    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    app = web.Application()
    app['config'] = config

    redis_pool = await setup_redis(app)
    setup_session(app, RedisStorage(redis_pool))

    loader = jinja2.PackageLoader('chat', 'templates')
    aiohttp_jinja2.setup(app, loader=loader, context_processors=[current_user_ctx_processor])

    # create connection to the database
    app.on_startup.append(init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_middlewares(app)

    db_pool = await init_pg(app)
    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(db_pool)
    )
    app['websockets'] = {}
    app.on_shutdown.append(shutdown)
    return app


async def setup_redis(app):
    pool = await aioredis.create_redis_pool((
        app['config']['redis']['host'],
        app['config']['redis']['port']
    ))

    async def close_redis():
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool


async def shutdown(app):
    for room in app['websockets'].values():
        for ws in room.values():
            await ws.close()
    app['websockets'].clear()


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


def main(argv):
    app = init(argv)
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app,
                host='localhost',
                port=8080)


if __name__ == '__main__':
    main(argv=sys.argv[1:])
