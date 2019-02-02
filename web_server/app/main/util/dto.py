from flask_restplus import fields

from app.main.controller.namespaces import user_ns, auth_ns, track_ns, room_ns
from app.main.model.track import TrackState, Track


class UserDto:
    user = user_ns.model('user', {
        'username': fields.String(required=True, description='user username'),
        'source': fields.String(description='user source')
    })


class AuthDto:
    user_auth = auth_ns.model('auth_details', {
        'username': fields.String(required=True, description='User login'),
        'password': fields.String(required=True, description='The user password '),
    })


class TrackDto:
    track_item = track_ns.model('track', {
        'id': fields.String(required=True, description='Song id'),
        'title': fields.String(required=True, description='Title'),
        'artist': fields.String(required=True, description='Artist'),
        'state': fields.String(required=True, enum=TrackState._member_names_, description='State')
    })


class RoomDto:
    room = room_ns.model('room', {
        'id': fields.String(required=True, description='Room id'),
        'name': fields.String(required=True, description='Room name')
    })

    room_creation = room_ns.model('room_creation', {
        'name': fields.String(required=True, description='Room name')
    })

    user_info = room_ns.model('user_info', {
        'id': fields.String(required=True, description='User id'),
        'username': fields.String(required=True, description='Username'),
    })

    member = room_ns.model('member', {
        'id': fields.String(required=True, description='Member id'),
        'level': fields.String(required=True, description='Member level'),
        'user': fields.Nested(user_info, description='User info')
    })

    room_full_info = room_ns.model('room_full_info', {
        'room': fields.Nested(room, description="Room info"),
        'members': fields.List(fields.Nested(member, description='Member info'))
    })
