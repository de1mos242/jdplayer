from flask import request
from flask_restplus import Resource

from app.main.controller.namespaces import auth_ns as api
from app.main.service.user_service import get_all_users, save_new_user, get_a_user
from app.main.util.decorator import admin_token_required
from app.main.util.dto import UserDto

user_dto = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @admin_token_required
    @api.marshal_list_with(user_dto, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user', security=None)
    @api.expect(user_dto, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


# noinspection PyUnresolvedReferences
@api.route('/<public_id>')
@api.param('public_id', 'The User ide ntifier')
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
