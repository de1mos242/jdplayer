import enum
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.main import db
from app.main.model.user import User


class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    playlist = relationship('Playlist', uselist=False)

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<room: {self.id}: {self.name}>'


class RoomMemberLevel(enum.Enum):
    admin = 'admin'
    participant = 'participant'


class RoomMember(db.Model):
    __tablename__ = 'room_members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(db.Enum(RoomMemberLevel), server_default=RoomMemberLevel.participant.value)
    room = relationship(Room.__name__)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user = relationship(User.__name__)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<member: {self.id}: {self.room_id} to {self.user_id}>'
