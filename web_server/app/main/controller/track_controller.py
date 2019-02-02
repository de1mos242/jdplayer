import flask_login
from flask import Response
from flask_restplus import Resource, reqparse

from app.main import vk_audio
from app.main.controller.namespaces import track_ns as api
from app.main.model.track import Track
from app.main.service import background_task_service
from app.main.service.track_service import get_all_cached_tracks, store_search_results
from app.main.util.dto import TrackDto

track_dto = TrackDto.track_item

search_tracks_query_arguments = api.parser()
search_tracks_query_arguments.add_argument('q', location='args')


@api.route('/')
class TracksListApi(Resource):
    @api.doc('Search in vk or list of all cached tracks', security=None)
    @api.marshal_list_with(track_dto, envelope='data')
    @api.expect(search_tracks_query_arguments, validate=True)
    @flask_login.login_required
    def get(self):
        parse_results = search_tracks_query_arguments.parse_args()
        if 'q' in parse_results and parse_results['q']:
            search_results = vk_audio.search_audio(parse_results['q'])
            return store_search_results(search_results)
        return get_all_cached_tracks()


@api.route('/<track_id>/playlist')
@api.param('track_id', 'track id', _in='path', required=True)
class TrackApi(Resource):
    # @api.route('/playlist')
    @api.doc("Add track to playlist", security=None)
    # @api.response(201, 'request accepted')
    def put(self, track_id):
        track = Track.query.get(track_id)
        background_task_service.download_track.delay(track.url, f'{track.id} - {track.artist}: {track.title}'[:30])
        return "job started"


@api.route('/play')
class StreamAudio(Resource):
    @api.doc("Get audio stream", security=None)
    def get(self):
        files = ['/home/denis/Загрузки/Sound_22272.mp3',
                 '/home/denis/Загрузки/Sound_22277.mp3',
                 '/home/denis/Загрузки/3 - Darude_ Sandstorm',
                 '/home/denis/Загрузки/test_upload_file.mp3']

        def generate():
            for f in files:
                with open(f, "rb") as fmp3:
                    data = fmp3.read(1024)
                    while data:
                        yield data
                        data = fmp3.read(1024)

        return Response(generate(), mimetype="audio/mp3")
