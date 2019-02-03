import random

from sqlalchemy import func

from app.main import db
from app.main.model.playlist import Playlist, PlaylistItem
from app.main.model.room import Room
from app.main.model.track import Track, TrackState
from app.main.service import track_service, background_task_service


def add_track_to_room(room: Room, track: Track):
    playlist = get_playlist_for_room(room)

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

    if track.state == TrackState.created:
        track_service.prepare_track_for_playlist(track, playlist)
    elif track.state == TrackState.ready:
        background_task_service.start_playing_in_room.delay(playlist.id)


def get_room_playlist_items(room):
    return PlaylistItem.query \
        .join(Playlist) \
        .filter(Playlist.room == room) \
        .order_by(PlaylistItem.position.asc()) \
        .all()


def pop_next_ready_track(playlist):
    playlist_item = PlaylistItem.query \
        .join(Track) \
        .filter(PlaylistItem.playlist == playlist) \
        .filter(Track.state == TrackState.ready) \
        .order_by(PlaylistItem.position.asc()) \
        .first()

    if not playlist_item:
        tracks_size = Track.query.filter(Track.state == TrackState.ready).with_only_columns([func.count()]).scalar()
        track_index = random.randint(0, tracks_size)
        track = Track.filter(Track.state == TrackState.ready).offset(track_index).first()
    else:
        track = playlist_item.track
        db.session.delete(playlist_item)
        db.session.commit()

    return track


def skip_current_track(room, current_user):
    playlist = get_playlist_for_room(room)
    background_task_service.skip_track(playlist.id, current_user.id)


def get_playlist_for_room(room):
    return Playlist.query.filter(Playlist.room == room).first()
