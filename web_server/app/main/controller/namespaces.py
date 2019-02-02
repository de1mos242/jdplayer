from flask_restplus import Namespace

user_ns = Namespace('user', description='user related operations')
auth_ns = Namespace('auth', description='authentication related operations')
track_ns = Namespace('track', description='track related operations')
room_ns = Namespace('room', description='room related operations')
