import asyncio

from app.main import celery
from app.main.model.track import Track
from app.main.service import track_service


@celery.task()
def download_track(track_id: int, playlist_id):
    track = Track.query.get(track_id)
    task = track_service.download_track(track, playlist_id)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(task)
