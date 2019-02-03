import os
import sys
import tempfile
import uuid
from typing import List

import aiohttp
from sqlalchemy.exc import SQLAlchemyError

from app.main import db, file_service
from app.main.model.track import Track, TrackState
from app.main.service import background_task_service
from app.main.service.audio_source.audio_search_result import AudioSearchResult
from app.main import stream_service


def get_all_cached_tracks() -> List[Track]:
    return Track.query.all()


def store_search_results(results: List[AudioSearchResult]) -> List[Track]:
    external_ids = [x.external_id for x in results]
    existed_tracks = Track.query.filter(Track.external_id.in_(external_ids)).all()
    existed_tracks_map = {x.external_id: x for x in existed_tracks}
    new_tracks_map = {
        x.external_id: Track(artist=x.artist,
                             title=x.title,
                             external_id=x.external_id,
                             duration=x.duration,
                             url=x.url)
        for x in results
        if x.external_id not in existed_tracks_map
    }

    db.session.add_all(new_tracks_map.values())
    db.session.commit()
    db_tracks_map = {**existed_tracks_map, **new_tracks_map}
    return list(map(lambda item: db_tracks_map[item.external_id], results))


async def download_track(track: Track, playlist_id):
    try:
        update_state(track, TrackState.downloading)
        target_name = f'{track.id} - {track.artist}: {track.title}'[:30] + f' - {uuid.uuid4()}'
        filepath = create_track_temp_filename()
        print(f'save file temporary in {filepath}')
        async with aiohttp.ClientSession() as session:
            async with session.get(track.url) as resp:
                data = await resp.read()
                with open(filepath, 'wb') as tmp:
                    tmp.write(data)

        file_service.upload_file(filepath, target_name)
        os.remove(filepath)
        track.binary_name = target_name
        update_state(track, TrackState.ready)
        if not stream_service.is_playing(playlist_id):
            stream_service.play_next(playlist_id)
    except SQLAlchemyError as err:
        db.session.rollback()
        track.error_data = str(err)
        update_state(track, TrackState.error)
        raise
    except:
        track.error_data = str(sys.exc_info()[0])
        update_state(track, TrackState.error)
        raise


def create_track_temp_filename():
    path = os.path.join(tempfile.mkdtemp(), 'jdplayer')
    os.mkdir(path)
    filename = f'{str(uuid.uuid4())}.mp3'
    filepath = os.path.join(path, filename)
    return filepath


def get_track(track_id):
    return Track.query.get(track_id)


def prepare_track_for_playlist(track, playlist):
    update_state(track, TrackState.pending)
    background_task_service.download_track.delay(track.id, playlist.id)


def update_state(track: Track, new_state: TrackState):
    track.state = new_state
    db.session.add(track)
    db.session.commit()
    db.session.flush()
