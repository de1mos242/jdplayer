from flask_restplus import fields

from app.main.controller.namespaces import user_ns, auth_ns, track_ns
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
