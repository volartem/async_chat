import aiopg.sa
import os
from aiohttp_security.abc import AbstractAuthorizationPolicy
from chat.models import get_user_by_username


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    def __init__(self, db_pool):
        self.db_pool = db_pool

    async def authorized_userid(self, identity):
        async with self.db_pool.acquire() as conn:
            user = await get_user_by_username(conn, identity)
            if user:
                return user

        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True


async def init_pg(app):
    engine = await aiopg.sa.create_engine(
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=int(os.environ.get('POSTGRES_PORT')),
        minsize=int(os.environ.get('POSTGRES_MIN_SIZE')),
        maxsize=int(os.environ.get('POSTGRES_MAX_SIZE')),
        loop=app.loop)
    app['models'] = engine
    return engine


async def close_pg(app):
    app['models'].close()
    await app['models'].wait_closed()
