import unittest

from app.main import db
from app.main.model.playlist import Playlist, PlaylistItem
from app.main.model.room import Room
from app.main.model.track import Track
from app.test.base import BaseTestCase


class TestPlaylistModel(BaseTestCase):
    def test_create_and_find_room_with_member(self):
        room = Room(name='test_room_name')
        track = Track(title="my mega track", duration=120,
                      artist='super artist', external_id=123)
        playlist = Playlist(room=room)
        playlist_item = PlaylistItem(playlist=playlist, track=track, position=12)

        db.session.add(room)
        db.session.add(track)
        db.session.add(playlist)
        db.session.add(playlist_item)
        db.session.commit()
        db.session.flush()

        db_item = PlaylistItem.query.filter(PlaylistItem.position == 12).first()

        self.assertIsNotNone(db_item, 'playlist item not found')
        self.assertEquals(db_item.playlist.room.name, 'test_room_name')
        self.assertEquals(db_item.track.title, 'my mega track')


if __name__ == '__main__':
    unittest.main()
