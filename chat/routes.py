from chat.views import index, login, logout, registration
from chat.rest_views import messages_id, messages_room_id, generate_uuid
from .websocket_views import websocket_handler
import pathlib
from weather.routes import setup_weather_routes

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    setup_weather_routes(app)
    app.router.add_get('/', index, name='index')
    app.router.add_get('/login', login, name='login')
    app.router.add_post('/login', login, name='login')
    app.router.add_get('/logout', logout, name='logout')
    app.router.add_get('/signup', registration, name='registration')
    app.router.add_post('/signup', registration, name='registration')
    app.router.add_get('/messages/{id}', messages_id)
    app.router.add_get('/messages/room/{id}', messages_room_id)
    app.router.add_get('/uuid/', generate_uuid)

    app.router.add_get("/ws/{room}/", websocket_handler)
    app.router.add_static('/static/',
                          path=str(PROJECT_ROOT / 'static'),
                          name='static')
