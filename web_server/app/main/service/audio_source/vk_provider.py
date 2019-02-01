import logging
from typing import List

import vk_api
from vk_api.audio import VkAudio

from app.main.service.audio_source.audio_search_result import AudioSearchResult


class VkProvider:

    def __init__(self, login: str = None, password: str = None) -> None:
        self.vk_audio = None
        if login and password:
            self.init_app(login, password)

    def init_app(self, login, password):
        if login != 'vk_login_not_set':
            self.vk_audio = self.__make_api(login, password)
        else:
            logging.warning('VK login password not set! Set corresponding environment variables')

    def search_audio(self, query: str) -> List[AudioSearchResult]:
        if self.vk_audio is None:
            return []
        songs = self.vk_audio.search(query)
        return list(map(
            lambda song: AudioSearchResult(title=song['title'],
                                           artist=song['artist'],
                                           duration=song['duration'],
                                           external_id=str(song['id']),
                                           url=song['url']),
            songs))

    def __make_api(self, login: str, password: str) -> VkAudio:
        print(f'login vk for {login}')
        vk_session = vk_api.vk_api.VkApi(login, password)
        vk_session.auth()
        return VkAudio(vk_session)
