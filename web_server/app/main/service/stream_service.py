import threading

import gi

from app.main import file_service, app

gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

from app.main.service.gstreamer_icecase_player import GstreamMountpoint


class StreamService:

    def __init__(self):
        Gst.init(None)
        GObject.threads_init()
        self.players = {}

    def play_next(self, playlist_id: int):
        from app.main.model.playlist import Playlist
        from app.main.service import playlist_service, track_service

        playlist = Playlist.query.get(playlist_id)
        playlist_item = playlist_service.get_next_ready_track(playlist)
        temp_filename = track_service.create_track_temp_filename()
        file_service.download_file(playlist_item.track.binary_name, temp_filename)
        if playlist.id not in self.players:
            self.start_thread(playlist, temp_filename)
        else:
            player = self.players[playlist.id]
            player.set_song(temp_filename)

    def start_thread(self, playlist, track_location):

        mount_point = GstreamMountpoint(f'/stream{playlist.id}.mp3',
                                        playlist_id=playlist.id,
                                        on_stop_callback=self.play_next_callback)
        thread = threading.Thread(target=mount_point.start,
                                  name=f'player_{playlist.id}',
                                  args=(track_location,))
        thread.start()
        self.players[playlist.id] = mount_point

    def play_next_callback(self, playlist_id: int):
        with app.app_context():
            self.play_next(playlist_id)

    def is_playing(self, playlist_id: int) -> bool:
        return playlist_id in self.players
