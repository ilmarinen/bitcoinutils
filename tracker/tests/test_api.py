import os
import unittest

from endpoint.config import basedir
from endpoint import app, db, gen_fixtures
from endpoint.models import models
from endpoint.models import api

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        gen_fixtures()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        _, token = api.signup("max", "Max", "Planck", "max@test.com", "test", False, send_email=False)
        user = api.get_user_by_username("max")
        assert(user is not None)
        assert(user.username == "max")
        assert(not user.is_active)

        _ = api.confirm_signup(token)

        user = api.get_user_by_username("max")
        assert (user.is_active)

    def test_authenticate(self):
        user = api.create_user("heisenberg", "Werner", "Heisenberg", "test@test.com", is_active=True)
        api.set_user_password(user, "test1")

        assert(not user.verify_password("test"))
        assert(user.verify_password("test1"))
