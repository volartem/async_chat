from third_party.views import weather_data, currency_data


def setup_third_party_routes(app):
    app.router.add_get('/weather', weather_data, name='weather')
    app.router.add_get('/currencies', currency_data, name='currency')
