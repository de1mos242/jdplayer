import unittest

from app.main import db
from app.main.model.track import Track
from app.test.base import BaseTestCase


class TestTrackModel(BaseTestCase):
    def test_hash_calculation(self):
        track = Track(title="my mega track", duration=120)
        track.fill_unique_id_by_track()
        db.session.add(track)
        db.session.commit()
        db.session.flush()

        self.assertIsNotNone(track.external_id, 'hash not calculated')


if __name__ == '__main__':
    unittest.main()
