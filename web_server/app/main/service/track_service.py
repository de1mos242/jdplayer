import os
import tempfile
import uuid
from typing import List

import aiohttp

from app.main import db, file_service
from app.main.model.track import Track
from app.main.service.audio_source.audio_search_result import AudioSearchResult


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


async def download_track(url: str, target_name):
    path = os.path.join(tempfile.mkdtemp(), 'jdplayer')
    os.mkdir(path)
    filename = f'{str(uuid.uuid4())}.mp3'
    filepath = os.path.join(path, filename)
    print(f'save file temporary in {filepath}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            with open(filepath, 'wb') as tmp:
                tmp.write(data)

    file_service.upload_file(filepath, target_name)
    os.remove(filepath)
