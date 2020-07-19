import os
import unittest
import json

from endpoint.config import basedir
from endpoint import app, db, gen_fixtures
from endpoint.models import api


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        gen_fixtures()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_and_logout(self):
        user = api.create_user("heisenberg", "Werner", "Heisenberg", "test@test.com", is_active=True)
        api.set_user_password(user, "test1")

        response = self.client.post(
            "api/v1/users/authenticate",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": "heisenberg", "password": "test1"}))

        assert(response.status_code == 200)
        assert(response.get_json() == True)

        response = self.client.get(
            "api/v1/users/authenticated")

        assert(response.status_code == 200)

        user_data = response.get_json()

        assert(user_data.get("username") == "heisenberg")

        self.client.post(
            "api/v1/users/logout",
            headers={"Content-Type": "application/json"})

        response = self.client.get(
            "api/v1/users/authenticated")

        assert(response.status_code == 401)
