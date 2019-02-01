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
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            self.create_user('t1000', '1000')

            # registered user login
            login_response = login_user(self, 't1000', '1000')
            self.assertEqual(login_response.status_code, 200)

    # def test_valid_logout(self):
    #     """ Test for logout before token expires """
    #     with self.client:
    #         self.create_user('t1000', '1000')
    #         login_response = login_user(self, 't1000', '1000')
    #         self.assertEqual(login_response.status_code, 200)
    #
    #         # valid token logout
    #         response = self.client.post(
    #             '/api/auth/logout',
    #             headers=dict(
    #
    #             )
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['status'] == 'success')
    #         self.assertEqual(response.status_code, 200)

    def create_user(self, username, password):
        user = User(username=username, source=UserSource.security)
        security_user = SecurityUser(username=username, user=user)
        security_user.password = password
        db.session.add(security_user)
        db.session.commit()
        db.session.flush()


if __name__ == '__main__':
    unittest.main()
