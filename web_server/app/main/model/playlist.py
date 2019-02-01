from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.main import db
from app.main.model.room import Room
from app.main.model.track import Track


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = relationship(Room.__name__)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<playlist: {self.id}: {self.room_id}>'


class PlaylistItem(db.Model):
    __tablename__ = 'playlist_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    playlist = relationship(Playlist.__name__)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)
    track = relationship(Track.__name__)
    position = db.Column(db.BigInteger, server_default='0')

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<playlist_item: {self.id} (room = {self.room_id} and track = {self.track_id} >'
