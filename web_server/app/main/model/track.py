import datetime
import enum

from sqlalchemy import func

from app.main import db


class TrackState(enum.Enum):
    created = 'created'
    pending = 'pending'
    downloading = 'downloading'
    ready = 'ready'
    error = 'error'


class Track(db.Model):
    """
    Model to storing tracks
    """
    __tablename__ = 'tracks'
    # __table_args__ = (UniqueConstraint('artist', 'title', 'duration'),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, unique=True)
    duration = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Enum(TrackState), server_default=TrackState.created.value)
    error_data = db.Column(db.Text)
    external_id = db.Column(db.String(200), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<track: {self.artist}: {self.title} ({str(datetime.timedelta(seconds=self.duration))})>'
