from typing import List

from app.main import db
from app.main.model.playlist import Playlist
from app.main.model.room import Room, RoomMember, RoomMemberLevel
from app.main.model.user import User


def create_room(name: str, creator: User) -> Room:
    room = Room(name=name)
    admin = RoomMember(level=RoomMemberLevel.admin, user=creator, room=room)
    playlist = Playlist(room=room)

    db.session.add(room)
    db.session.add(admin)
    db.session.add(playlist)
    db.session.commit()

    return room


def get_rooms(user: User) -> List[Room]:
    member_query_filter = RoomMember.query.filter(RoomMember.user == user).with_entities(RoomMember.id)
    return Room.query.filter(Room.id.in_(member_query_filter)).all()


def get_room_full_info(room_id, user):
    db_info = db.session.query(Room, RoomMember).join(RoomMember.room).filter(Room.id == room_id).filter(
        RoomMember.user == user).all()
    return {'room': db_info[0][0],
            'members': [info[1] for info in db_info]}


def get_room(room_id, user):
    return Room.query.filter(Room.id.in_(
        RoomMember.query
            .filter(RoomMember.room_id == room_id)
            .filter(RoomMember.user == user)
            .with_entities(RoomMember.room_id)
    )).first()
