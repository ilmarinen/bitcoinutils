from flask_login import current_user
from endpoint.lib.http import permission, APIException
from endpoint.models import api


@permission
def can_view_restaurants(*args, **kwargs):
    if not current_user.is_authenticated:
        return False

    return True


@permission
def can_create_restaurant():
    if not current_user.is_authenticated:
        return False

    if api.is_restaurant_owner(current_user):
        return True
    
    return False


@permission
def can_edit_restaurant(restaurant_id):
    if not current_user.is_authenticated:
        return False

    restaurant = api.get_restaurant(restaurant_id)
    if current_user.id == restaurant.owner_id:
        return True
    
    return False


@permission
def can_create_edit_and_delete_restaurant_meals(restaurant_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    restaurant = api.get_restaurant(restaurant_id)
    if current_user.id == restaurant.owner_id:
        return True

    return False


@permission
def can_view_restaurant_meals(restaurant_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    return True


@permission
def can_list_restaurant_orders(restaurant_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    restaurant = api.get_restaurant(restaurant_id)
    if current_user.id == restaurant.owner_id:
        return True

    return False


@permission
def can_create_restaurant_orders(restaurant_id, *args, **kwargs):
    if not current_user.is_authenticated:
        return False

    return True
