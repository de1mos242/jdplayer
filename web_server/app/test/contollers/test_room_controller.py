import json
import unittest

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


def create_room(self, room_name):
    return self.client.post(
        '/api/room/',
        data=json.dumps({'name': room_name}),
        content_type='application/json'
    )


class TestRoomController(BaseTestCase):

    def test_create_room(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            self.create_user('t1000', '1000')

            # registered user login
            login_response = login_user(self, 't1000', '1000')
            self.assertEqual(login_response.status_code, 200)

            create_room_response = create_room(self, 'test_room')
            self.assertEqual(create_room_response.status_code, 200)
            data = json.loads(create_room_response.data.decode())
            self.assertTrue(data['data']['name'] == 'test_room')


if __name__ == '__main__':
    unittest.main()
