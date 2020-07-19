from flask.views import View, MethodView
from flask import send_from_directory, abort, make_response, request
import os.path as ospath
from functools import wraps
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response
import json


class APIException(HTTPException):
    def __init__(self, code, message):
        self.code = code
        self.description = message

    def get_body(self, environ=None):
        return json.dumps({'message': self.description})

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    def get_response(self, environ=None):
        return Response(self.get_body(), self.code, self.get_headers())


def expose_static_files(app):
    base_folder = ospath.abspath(
        ospath.join(ospath.dirname(__file__), '../../../../client/public/'))

    @app.route('/public/<path:path>')
    def send_static_files(path):
        try:
            return send_from_directory(base_folder, path)
        except:
            abort(404)


def no_cache(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] =\
            'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return decorated_function


def permission(func):
    @wraps(func)
    def with_permission(request_handler):
        @wraps(request_handler)
        def with_request_handler(*args, **kwargs):
            if func(**kwargs):
                return request_handler(*args, **kwargs)
            else:
                raise APIException(401, 'Unauthorized')

        return with_request_handler

    return with_permission


class BaseView(View):

    def make_response(self, result):
        return make_response(result)

    def dispatch_request(self, *args, **kwargs):
        result = super(BaseView, self).dispatch_request(*args, **kwargs)
        return self.make_response(result)


class RESTView(MethodView):
    def make_response(self, result):
        if (request.method == 'POST' and
                request.headers.get('Content-Type').upper() not in
                [
                    'application/json'.upper(),
                    'application/json;charset=utf-8'.upper()]):
            raise APIException(400, 'Bad request')
        else:
            response = make_response(json.dumps(result))
            response.headers['Content-Type'] = 'application/json'
            return response

    def dispatch_request(self, *args, **kwargs):
        result = super(RESTView, self).dispatch_request(*args, **kwargs)
        return self.make_response(result)
