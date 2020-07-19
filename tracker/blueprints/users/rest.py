from tracker.lib.http import RESTView, APIException
from tracker.lib import formatter
from tracker.blueprints.users import data_format
from flask import Blueprint, request
from tracker.models import api
from flask_login import current_user, logout_user
from tracker.blueprints.users import permissions
from tracker.models import formatting


bp = Blueprint('user_rest_views', __name__, template_folder='templates')


class AuthenticationUserAPI(RESTView):

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        authenticated = api.authenticate(username, password)
        if not authenticated:
            raise APIException(401, "Unauthorized")

        return authenticated


class LogoutUserAPI(RESTView):

    def post(self):
        logout_user()
        return True


class AuthenticatedUserAPI(RESTView):

    def get(self):
        if not current_user.is_authenticated:
            raise APIException(401, "Unauthorized")
        user_data = formatter.make(current_user, formatting.user_format)

        return user_data

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if api.authenticate(username, password):
            user_data = formatter.make(current_user, formatting.user_format)

            return user_data

        raise APIException(401, "Incorrect login")


class UserModelAPI(RESTView):

    def get(self, user_id):
        return "UserModelAPI GET"

    @permissions.can_update_user
    def put(self, user_id):
        user_data = request.get_json()
        firstname = user_data.get("firstname")
        lastname = user_data.get("lastname")
        api.update_user(user_id, firstname, lastname)
        user_data = formatter.make(current_user, data_format.user_format)

        return user_data


class UsersAPI(RESTView):

    def get(self, **kwargs):
        return "UsersAPI GET"


class UserAddressesAPI(RESTView):

    @permissions.can_list_addresses_and_transactions
    def get(self, user_id, **kwargs):
        addresses_data = list(
            map(
                lambda address: formatter.make(
                    address, formatting.address_format),
                api.get_user_addresses(user_id)))
        return addresses_data

    @permissions.can_list_addresses_and_transactions
    def post(self, user_id, **kwargs):
        data = request.get_json()
        address_string = data.get("address")
        address = api.get_or_create_address(user_id, address_string)
        address_data = formatter.make(address, formatting.address_format)

        return address_data


class UserAddressesModelAPI(RESTView):

    @permissions.can_list_addresses_and_transactions
    def get(self, user_id, address_id, **kwargs):
        address = api.get_user_address(user_id, address_id)
        if address is None:
            raise APIException(404, 'Not found')
        address_data = formatter.make(address, formatting.address_format)
        return address_data


class UserAddressesModelUpdateAPI(RESTView):

    @permissions.can_list_addresses_and_transactions
    def get(self, user_id, address_id, **kwargs):
        address = api.get_user_address(user_id, address_id)
        if address is None:
            raise APIException(404, 'Not found')
        address = api.update_user_address(user_id, address_id)
        address_data = formatter.make(address, formatting.address_format)
        return address_data


class UserAddressTransactionsAPI(RESTView):

    @permissions.can_list_addresses_and_transactions
    def get(self, user_id, address_id, **kwargs):
        address = api.get_user_address(user_id, address_id)
        if address is None:
            raise APIException(404, 'Not found')

        address_transactions = api.get_user_address_transactions(user_id, address_id)
        address_transactions_data = list(map(
            lambda adtx: formatter.make(adtx, formatting.address_transaction_format),
            address_transactions))

        return address_transactions_data


class UserAddressTransactionsModelAPI(RESTView):

    @permissions.can_list_addresses_and_transactions
    def get(self, user_id, address_id, address_transaction_id, **kwargs):
        address = api.get_user_address(user_id, address_id)
        if address is None:
            raise APIException(404, 'Not found')
        address_transaction = api.get_address_transaction(address_transaction_id)
        address_transaction_data = formatter.make(address_transaction, formatting.address_transaction_format)

        return address_transaction_data


bp.add_url_rule(
    '/v1/users/authenticated',
    view_func=AuthenticatedUserAPI.as_view('authenticated_user_api'))
bp.add_url_rule(
    '/v1/users/authenticate',
    view_func=AuthenticationUserAPI.as_view('authentication_user_api'))
bp.add_url_rule(
    '/v1/users/logout',
    view_func=LogoutUserAPI.as_view('logout_user_api'))
bp.add_url_rule(
    '/v1/users/<int:user_id>',
    view_func=UserModelAPI.as_view('user_model_api'))
bp.add_url_rule(
    '/v1/users',
    view_func=UsersAPI.as_view('users_view'))
bp.add_url_rule(
    '/v1/users/<int:user_id>/addresses',
    view_func=UserAddressesAPI.as_view('user_addresses_view'))
bp.add_url_rule(
    '/v1/users/<int:user_id>/addresses/<int:address_id>',
    view_func=UserAddressesModelAPI.as_view('user_addresses_model_view'))
bp.add_url_rule(
    '/v1/users/<int:user_id>/addresses/<int:address_id>/get_updates',
    view_func=UserAddressesModelUpdateAPI.as_view('user_addresses_model_update_view'))
bp.add_url_rule(
    '/v1/users/<int:user_id>/addresses/<int:address_id>/transactions',
    view_func=UserAddressTransactionsAPI.as_view('user_address_transactions_view'))
bp.add_url_rule(
    '/v1/users/<int:user_id>/addresses/<int:address_id>/transactions/<int:address_transaction_id>',
    view_func=UserAddressTransactionsModelAPI.as_view('user_address_transactions_model_view'))
