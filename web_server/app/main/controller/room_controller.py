import flask_login
from flask import request
from flask_restplus import Resource

from app.main.controller.namespaces import room_ns as api
from app.main.service import room_service
from app.main.util.dto import RoomDto

room_dto = RoomDto.room


@api.route('/')
class RoomsListApi(Resource):

    @api.doc('Create new room')
    @api.marshal_with(room_dto, envelope='data')
    @api.expect(RoomDto.room_creation)
    @flask_login.login_required
    def post(self):
        name = request.json['name']
        current_user = flask_login.current_user
        room = room_service.create_room(name, current_user)
        return room

    @api.doc('Get available rooms')
    @api.marshal_list_with(room_dto, envelope='data')
    @flask_login.login_required
    def get(self):
        current_user = flask_login.current_user
        return room_service.get_rooms(current_user)


@api.route('/<room_id>')
@api.param('room_id', 'room id', _in='path', required=True)
class RoomApi(Resource):

    @api.doc("Get room info", security=None)
    @api.marshal_with(RoomDto.room_full_info, envelope='data')
    @flask_login.login_required
    def get(self, room_id):
        current_user = flask_login.current_user
        full_info = room_service.get_room_full_info(room_id, current_user)
        return full_info
