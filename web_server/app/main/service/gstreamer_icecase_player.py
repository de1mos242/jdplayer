import os
import threading
import time

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject


class GstreamMountpoint(object):

    def __init__(self, mount_point):
        self.playmode = False

        self.pipeline = Gst.Pipeline.new(f'main-pipe-{mount_point}')
        self.file_src = Gst.ElementFactory.make('filesrc', 'file_source')
        self.audio_parse = Gst.ElementFactory.make('mpegaudioparse', 'audio_parse')
        self.decoder = Gst.ElementFactory.make('mpg123audiodec', 'mp3_decoder')
        self.shoutcast_queue = Gst.ElementFactory.make('queue', 'sh_queue')
        self.audio_convert = Gst.ElementFactory.make('audioconvert', 'audio_convert')
        self.lame = Gst.ElementFactory.make('lamemp3enc', 'lame')
        self.lame.set_property('bitrate', 192)

        self.tag_inject = Gst.ElementFactory.make('taginject', 'tag_inject')
        self.shoutcast = Gst.ElementFactory.make('shout2send', 'shout_to_send')
        self.shoutcast.set_property('ip', 'localhost')
        self.shoutcast.set_property('port', 8000)
        self.shoutcast.set_property('password', 'icejdplayer')
        self.shoutcast.set_property('mount', mount_point)
        self.shoutcast.set_property('url', f'localhost:8000{mount_point}')

        self.pipeline.add(self.file_src)
        self.pipeline.add(self.audio_parse)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.shoutcast_queue)
        self.pipeline.add(self.audio_convert)
        self.pipeline.add(self.lame)
        self.pipeline.add(self.tag_inject)
        self.pipeline.add(self.shoutcast)

        self.file_src.link(self.audio_parse)
        self.audio_parse.link(self.decoder)
        self.decoder.link(self.shoutcast_queue)
        self.shoutcast_queue.link(self.audio_convert)
        self.audio_convert.link(self.lame)
        self.lame.link(self.tag_inject)
        self.tag_inject.link(self.shoutcast)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            print(f'Get end of file, exit in {threading.current_thread().name}')
            self.playmode = False
        elif t == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            print(err)
            print(debug)
            self.playmode = False

    def start(self, filepath):
        if os.path.isfile(filepath):
            filepath = os.path.realpath(filepath)
            self.playmode = True
            print(f"play {filepath} in {threading.current_thread().name}")
            self.file_src.set_property('location', filepath)
            self.pipeline.set_state(Gst.State.PLAYING)
            while self.playmode:
                time.sleep(1)
            print(f"stop playing {filepath} in {threading.current_thread().name}")

    def stop(self):
        self.playmode = False

    def set_song(self, filepath):
        if os.path.isfile(filepath):
            filepath = os.path.realpath(filepath)
            print(f"change song to {filepath} in {threading.current_thread().name}")
            self.pipeline.set_state(Gst.State.READY)
            self.file_src.set_property('location', filepath)
            self.pipeline.set_state(Gst.State.PLAYING)
            print(f"song changed {filepath} in {threading.current_thread().name}")


def run():
    GObject.threads_init()
    Gst.init(None)
    players = []
    for i in range(10):
        mount_point = GstreamMountpoint(f'/stream{i}.mp3')
        thread = threading.Thread(target=mount_point.start,
                                  name=f'player_{i}',
                                  args=('/home/denis/Загрузки/3 - Darude_ Sandstorm',))
        time.sleep(0.2)
        thread.start()
        players.append(mount_point)

    # loop = GLib.MainLoop()
    # loop.run()

    # threading.Thread(target=loop.run)

    input('anykey to exit...')
    for p in players:
        p.set_song('/home/denis/Загрузки/test_upload_file.mp3')


    input('anykey to exit...')
    for p in players:
        p.stop()


if __name__ == '__main__':
    run()
