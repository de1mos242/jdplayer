import unittest

from app.main import db
from app.main.model.track import Track
from app.test.base import BaseTestCase


class TestTrackModel(BaseTestCase):
    def test_hash_calculation(self):
        track = Track(title="my mega track", duration=120,
                      artist='super artist', external_id=123)
        db.session.add(track)
        db.session.commit()
        db.session.flush()

        db_track = Track.query.filter(Track.title == 'my mega track').first()
        self.assertIsNotNone(db_track, 'track not saved')


if __name__ == '__main__':
    unittest.main()
