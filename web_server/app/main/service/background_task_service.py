import asyncio

from app.main import celery
from app.main.service import track_service


@celery.task()
def download_track(url: str, target_name: str):
    task = track_service.download_track(url, target_name)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(task)
