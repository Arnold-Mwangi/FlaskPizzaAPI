#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    response_dict = {"message": "Welcome to Pizza Inn"}
    return make_response(jsonify(response_dict), 200)

class Restaurants(Resource):

    def get(self):
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response(jsonify(restaurants), 200)

class RestaurantsByID(Resource):

    def get(self, id):
        restaurant =  Restaurant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(restaurant), 200)
    
    def delete(self, id):
        restaurant = Restaurant.query.get(id)

        if restaurant is None:
        # Return an error response indicating that the restaurant was not found
            response_dict = {
                "message": f'Restaurant of id {id} not found',
            }
            return make_response(jsonify(response_dict), 404)

        deleted_pizzas = []

        for pizza in restaurant.pizzas:
            deleted_pizzas.append({
                "pizza_id": pizza.pizza_id,
                "restaurant_id": pizza.restaurant_id
            })
            db.session.delete(pizza)

        db.session.delete(restaurant)
        db.session.commit()
        
        response_dict = {
            "message": f'Restaurant of id {id} deleted Successfully',
            "deleted_pizzas": deleted_pizzas
        }
        return make_response(jsonify(response_dict),200)

api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantsByID, '/restaurants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)