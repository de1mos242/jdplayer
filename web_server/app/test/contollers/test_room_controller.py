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


def get_tracks_from_cache(self):
    return self.client.get('/api/track/')


def order_track_in_room(self, room_id, track_id):
    return self.client.put(f'/api/room/{room_id}/track/{track_id}')


def get_playlist_items_in_room(self, room_id):
    return self.client.get(f'/api/room/{room_id}/playlist/')


class TestRoomController(BaseTestCase):

    def test_create_room(self):
        with self.client:
            self.create_user('t1000', '1000')
            login_response = login_user(self, 't1000', '1000')
            self.assertEqual(login_response.status_code, 200)

            create_room_response = create_room(self, 'test_room')
            self.assertEqual(create_room_response.status_code, 200)
            data = json.loads(create_room_response.data.decode())
            self.assertTrue(data['data']['name'] == 'test_room')

    def test_order_tracks(self):
        with self.client:
            self.create_user('t1000', '1000')
            login_user(self, 't1000', '1000')
            create_room_response = create_room(self, 'test_room')
            data = json.loads(create_room_response.data.decode())
            room_id = data['data']['id']
            self.create_track('a1', 't1', 60, 'ext1')
            self.create_track('a2', 't2', 120, 'ext2')

            cached_tracks_response = get_tracks_from_cache(self)
            self.assertEqual(cached_tracks_response.status_code, 200)
            data = json.loads(cached_tracks_response.data.decode())
            t1_id = next((t['id'] for t in data['data'] if t['title'] == 't1'))
            t2_id = next((t['id'] for t in data['data'] if t['title'] == 't2'))

            order_t1_response = order_track_in_room(self, room_id, t1_id)
            self.assertEqual(order_t1_response.status_code, 200)

            # should do nothing
            order_t1_dup_response = order_track_in_room(self, room_id, t1_id)
            self.assertEqual(order_t1_dup_response.status_code, 200)

            order_t2_response = order_track_in_room(self, room_id, t2_id)
            self.assertEqual(order_t2_response.status_code, 200)

            items_response = get_playlist_items_in_room(self, room_id)
            self.assertEqual(items_response.status_code, 200)

            data = json.loads(items_response.data.decode())['data']
            self.assertEqual(data[0]['track']['title'], 't1')
            self.assertEqual(data[0]['position'], 1)
            self.assertEqual(data[1]['track']['title'], 't2')
            self.assertEqual(data[1]['position'], 2)


if __name__ == '__main__':
    unittest.main()
