import asyncio

from app.main import celery, stream_service
from app.main.model.track import Track
from app.main.service import track_service


@celery.task()
def download_track(track_id: int, playlist_id: int):
    track = Track.query.get(track_id)
    task = track_service.download_track(track)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(task)
    stream_service.start_if_not_playing(playlist_id)


@celery.task()
def start_playing_in_room(playlist_id: int):
    stream_service.start_if_not_playing(playlist_id)


@celery.task()
def skip_track(playlist_id: int, user_id: int):
    stream_service.skip_track(playlist_id, user_id)
