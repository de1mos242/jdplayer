import unittest

from app.main import db
from app.main.model.room import Room, RoomMember, RoomMemberLevel
from app.main.model.user import User, UserSource
from app.test.base import BaseTestCase


class TestRoomModel(BaseTestCase):
    def test_create_and_find_room_with_member(self):
        room = Room(name='test_room_name')
        user = User(username="test username", source=UserSource.security)
        member = RoomMember(user=user, room=room, level=RoomMemberLevel.admin)

        db.session.add(room)
        db.session.add(user)
        db.session.add(member)
        db.session.commit()
        db.session.flush()

        room_from_db = Room.query.filter(Room.name == 'test_room_name').first()
        self.assertIsNotNone(room_from_db, 'room not saved')

        member_from_db = RoomMember.query.filter(RoomMember.room == room_from_db).first()
        self.assertIsNotNone(member_from_db, 'member not saved')

        self.assertEquals(member_from_db.user.username, 'test username')
        self.assertEquals(member_from_db.room.name, 'test_room_name')
        self.assertEquals(member_from_db.level, RoomMemberLevel.admin)


if __name__ == '__main__':
    unittest.main()
