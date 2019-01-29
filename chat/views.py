import aiohttp_jinja2
from .models import get_all_rooms, get_user_by_username, create_user
from .form import validate_login_form, validate_signup_form
from aiohttp_security import remember, forget, authorized_userid
from aiohttp import web


@aiohttp_jinja2.template('index.html')
async def index(request):
    username = await authorized_userid(request)
    if username:
        print(username)
    async with request.app['models'].acquire() as conn:
        rooms = await get_all_rooms(conn)
        return {'rooms': rooms, 'user': username}


@aiohttp_jinja2.template('login.html')
async def login(request):
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')

    if request.method == 'POST':
        form = await request.post()

        async with request.app['models'].acquire() as conn:
            error = await validate_login_form(conn, form)

            if error:
                return {'error': error}
            else:
                response = redirect(request.app.router, 'index')

                user = await get_user_by_username(conn, form['username'])
                await remember(request, response, user['username'])

                raise response
    return {}


@aiohttp_jinja2.template('registration.html')
async def registration(request):
    username = await authorized_userid(request)
    if username:
        raise redirect(request.app.router, 'index')

    if request.method == 'POST':
        form = await request.post()

        async with request.app['models'].acquire() as conn:
            error = await validate_signup_form(conn, form)

            if error:
                return {'error': error}
            else:
                response = redirect(request.app.router, 'index')

                user = await create_user(conn, form)
                await remember(request, response, user['username'])

                raise response
    return {}


async def logout(request):
    response = redirect(request.app.router, 'login')
    await forget(request, response)
    return response


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)
