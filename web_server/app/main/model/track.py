import datetime
import enum
import hashlib

from sqlalchemy import UniqueConstraint, func, event

from app.main import db


class TrackState(enum.Enum):
    pending = 'pending'
    downloading = 'downloading'
    ready = 'ready'
    error = 'error'


class Track(db.Model):
    """
    Model to storing tracks
    """
    __tablename__ = 'tracks'
    __table_args__ = (UniqueConstraint('title', 'duration'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, unique=True)
    duration = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Enum(TrackState))
    error_data = db.Column(db.Text)
    unique_id = db.Column(db.String(200), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<track: {self.title} ({str(datetime.timedelta(seconds=self.duration))})'

    def fill_unique_id_by_track(self):
        self.unique_id = Track.calculate_unique_id(self.title, self.duration)

    @staticmethod
    def calculate_unique_id(title: str, duration: int) -> str:
        """
        calculate unique_id by title and duration if not unique id exists
        :return:
        """
        h = hashlib.sha256()
        h.update(str.encode(title))
        h.update(bytes(duration))
        return h.hexdigest()
