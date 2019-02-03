import flask_login
from flask import request
from flask_restplus import Resource

from app.main.controller.namespaces import room_ns as api
from app.main.service import room_service, track_service, playlist_service
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

    @api.doc("Get room info")
    @api.marshal_with(RoomDto.room_full_info, envelope='data')
    @flask_login.login_required
    def get(self, room_id):
        current_user = flask_login.current_user
        if not room_service.get_room(room_id, current_user):
            return 'Room not found', 404
        full_info = room_service.get_room_full_info(room_id)
        return full_info


@api.route('/<room_id>/playlist/')
@api.param('room_id', 'room id', _in='path', required=True)
class RoomTracksApi(Resource):

    @api.doc("Get playlist items in room")
    @api.marshal_list_with(RoomDto.playlist_item, envelope='data')
    @flask_login.login_required
    def get(self, room_id):
        current_user = flask_login.current_user
        room = room_service.get_room(room_id, current_user)
        if not room:
            return 'Room not found', 404

        items = playlist_service.get_room_playlist_items(room)
        return items


@api.route('/<room_id>/track/<track_id>')
@api.param('room_id', 'room id', _in='path', required=True)
@api.param('track_id', 'track id', _in='path', required=True)
class RoomOrderTrackApi(Resource):

    @api.doc("Order track in room")
    @flask_login.login_required
    def put(self, room_id, track_id):
        current_user = flask_login.current_user
        room = room_service.get_room(room_id, current_user)
        if not room:
            return 'Room not found', 404
        track = track_service.get_track(track_id)
        if not track:
            return 'Track not found', 404

        playlist_service.add_track_to_room(room, track)
        return 'added', 200


@api.route('/<room_id>/track/')
@api.param('room_id', 'room id', _in='path', required=True)
class RoomTracksApi(Resource):

    @api.doc("Skip current track in room")
    @flask_login.login_required
    def delete(self, room_id):
        current_user = flask_login.current_user
        room = room_service.get_room(room_id, current_user)
        if not room:
            return 'Room not found', 404

        playlist_service.skip_current_track(room, current_user)
        return "skip added"
