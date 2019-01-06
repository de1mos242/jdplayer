from flask_restplus import Namespace

user_ns = Namespace('user', description='user related operations')
auth_ns = Namespace('auth', description='authentication related operations')
