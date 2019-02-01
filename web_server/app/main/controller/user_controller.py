import logging

import flask_login
from flask import g
from flask_login import login_required
from flask_restplus import Resource

from app.main.controller.namespaces import user_ns as api
from app.main.service.user_service import get_all_users
from app.main.util.dto import UserDto

user_dto = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @flask_login.login_required
    @api.marshal_list_with(user_dto, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()


# noinspection PyUnresolvedReferences
@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user', security=None)
    @api.marshal_with(user_dto)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
