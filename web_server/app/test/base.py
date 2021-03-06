from flask_testing import TestCase

from app.main import db, app
from app.main.config import Config
from app.main.model.track import Track
from app.main.model.user import User, UserSource, SecurityUser


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(Config)
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def create_user(username, password):
        user = User(username=username, source=UserSource.security)
        security_user = SecurityUser(username=username, user=user)
        security_user.password = password
        db.session.add(security_user)
        db.session.commit()
        db.session.flush()

    @staticmethod
    def create_track(artist, title, duration, external_id, url=None):
        track = Track(artist=artist, title=title,
                      duration=duration, external_id=external_id,
                      url=url)
        db.session.add(track)
        db.session.commit()
        db.session.flush()
        return track
