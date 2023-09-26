import json
from models import db, Pizza, Restaurant, RestaurantPizza
from app import app



class TestPizzaRoutes():

    def test_pizza_route(self):
        response = app.test_client().get('/pizzas')
        assert(response.status_code == 200)