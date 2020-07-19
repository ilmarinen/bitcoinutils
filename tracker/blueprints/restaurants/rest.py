from endpoint.lib.http import RESTView, BaseView, APIException
from endpoint.lib import formatter
from endpoint.blueprints.restaurants import data_format, permissions
from flask import Blueprint, request, session, render_template
from endpoint.models import api, formatting
from flask_login import current_user, logout_user


bp = Blueprint('restaurant_rest_views', __name__, template_folder='templates')


class RestaurantsAPI(RESTView):

    @permissions.can_view_restaurants
    def get(self, **kwargs):
        restaurants = api.list_restaurants()
        return list(map(formatting.build_restaurant_json, restaurants))

    @permissions.can_create_restaurant
    def post(self, **kwargs):
        restaurant_data = request.get_json()
        name = restaurant_data.get("name")
        description = restaurant_data.get("description")
        owner_id = current_user.id
        restaurant = api.create_restaurant(name, description, owner_id)

        return formatter.make(restaurant, data_format.restaurant_format)


class RestaurantModelAPI(RESTView):

    @permissions.can_view_restaurants
    def get(self, restaurant_id):
        restaurant = api.get_restaurant(restaurant_id)
        restaurant_data = formatting.build_restaurant_json(restaurant)
        return restaurant_data

    @permissions.can_edit_restaurant
    def put(self, restaurant_id):
        restaurant_data = request.get_json()
        name = restaurant_data.get("name")
        description = restaurant_data.get("description")
        restaurant = api.update_restaurant(restaurant_id, name, description)
        return formatting.build_restaurant_json(restaurant)

    @permissions.can_edit_restaurant
    def delete(self, restaurant_id):
        api.delete_restaurant(restaurant_id)
        return True


class MealAPI(RESTView):

    @permissions.can_view_restaurant_meals
    def get(self, restaurant_id):
        meals = api.list_restaurant_meals(restaurant_id)
        return list(map(lambda meal: formatter.make(meal, formatting.meal_format), meals))

    @permissions.can_create_edit_and_delete_restaurant_meals
    def post(self, restaurant_id):
        meal_data = request.get_json()
        name = meal_data.get("name")
        description = meal_data.get("description")
        price = meal_data.get("price")
        meal = api.create_restaurant_meal(restaurant_id, name, description, price)
        return formatter.make(meal, formatting.meal_format)


class MealModelAPI(RESTView):

    @permissions.can_view_restaurant_meals
    def get(self, restaurant_id, meal_id):
        meal = api.get_restaurant_meal(restaurant_id, meal_id)
        return formatter.make(meal, formatting.meal_format)

    @permissions.can_create_edit_and_delete_restaurant_meals
    def put(self, restaurant_id, meal_id):
        meal_data = request.get_json()
        name = meal_data.get("name")
        description = meal_data.get("description")
        price = meal_data.get("price")
        meal = api.update_restaurant_meal(restaurant_id, meal_id, name, description, price)
        return formatter.make(meal, formatting.meal_format)

    @permissions.can_create_edit_and_delete_restaurant_meals
    def delete(self, restaurant_id, meal_id):
        api.delete_restaurant_meal(restaurant_id, meal_id)
        return True


class RestaurantOrderAPI(RESTView):

    @permissions.can_list_restaurant_orders
    def get(self, restaurant_id):
        orders = api.list_restaurant_orders(restaurant_id)
        return list(map(formatting.build_order_json, [order.id for order in orders]))

    @permissions.can_create_restaurant_orders
    def post(self, restaurant_id):
        order_data = request.get_json()
        meal_ids = order_data.get("meal_ids")
        order = api.create_restaurant_order(restaurant_id, meal_ids, current_user.id)
        return formatting.build_order_json(order)

bp.add_url_rule('/v1/restaurants/', view_func=RestaurantsAPI.as_view('restaurants_view'))
bp.add_url_rule('/v1/restaurants/<int:restaurant_id>', view_func=RestaurantModelAPI.as_view('restaurant_model_view'))
bp.add_url_rule('/v1/restaurants/<int:restaurant_id>/meals', view_func=MealAPI.as_view('meals_view'))
bp.add_url_rule('/v1/restaurants/<int:restaurant_id>/meals/<int:meal_id>', view_func=MealModelAPI.as_view('meal_model_view'))
bp.add_url_rule('/v1/restaurants/<int:restaurant_id>/orders', view_func=RestaurantOrderAPI.as_view('restaurant_orders_view'))
