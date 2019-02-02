from app.main import db
from app.main.model.playlist import Playlist, PlaylistItem
from app.main.model.room import Room
from app.main.model.track import Track


def add_track_to_room(room: Room, track: Track):
    playlist = Playlist.query.filter(Playlist.room == room).first()

    playlist_item = PlaylistItem.query \
        .filter(PlaylistItem.playlist == playlist) \
        .filter(PlaylistItem.track == track) \
        .first()

    if not playlist_item:
        last_position = (PlaylistItem.query
                         .filter(PlaylistItem.playlist == playlist)
                         .with_entities(PlaylistItem.position)
                         .order_by(PlaylistItem.position.desc())
                         .first() or (0,))[0]
        playlist_item = PlaylistItem(playlist=playlist, track=track, position=last_position + 1)
        db.session.add(playlist_item)
        db.session.commit()


def get_room_playlist_items(room):
    return PlaylistItem.query \
        .join(Playlist) \
        .filter(Playlist.room == room) \
        .order_by(PlaylistItem.position.asc()) \
        .all()
