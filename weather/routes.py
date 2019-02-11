from weather.views import weather_data


def setup_weather_routes(app):
    app.router.add_get('/weather', weather_data, name='weather')
