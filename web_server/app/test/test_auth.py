import json
import unittest

from app.main import db
from app.main.model.user import User, SecurityUser, UserSource
from app.test.base import BaseTestCase


def login_user(self, username, password):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):

    def test_registered_user_login(self):
        with self.client:
            # user registration
            self.create_user('t1000', '1000')

            # registered user login
            login_response = login_user(self, 't1000', '1000')
            self.assertEqual(login_response.status_code, 200)

    def test_valid_logout(self):
        with self.client:
            self.create_user('t1000', '1000')
            login_response = login_user(self, 't1000', '1000')
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            response = self.client.post(
                '/api/auth/logout'
            )
            self.assertEqual(response.status_code, 200)

            unauth_access_response = self.client.get(
                '/api/room/1'
            )
            self.assertEqual(unauth_access_response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
