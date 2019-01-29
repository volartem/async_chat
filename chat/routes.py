from chat.views import index, login, logout, registration
from chat.rest_views import messages_id, messages_room_id
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', index, name='index')
    app.router.add_get('/login', login, name='login')
    app.router.add_post('/login', login, name='login')
    app.router.add_get('/logout', logout, name='logout')
    app.router.add_get('/signup', registration, name='registration')
    app.router.add_post('/signup', registration, name='registration')
    app.router.add_get('/messages/{id}', messages_id)
    app.router.add_get('/messages/room/{id}', messages_room_id)
    app.router.add_static('/static/',
                          path=str(PROJECT_ROOT / 'static'),
                          name='static')
