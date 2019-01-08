import urllib
from pprint import pprint

import aiohttp
from typing import List

import vk_api
from vk_api.audio import VkAudio

from app.main.service.audio_source.audio_search_result import AudioSearchResult


class VkProvider:

    def __init__(self, token: str) -> None:
        self.token = token
        self.url = "http://vk.com/al_search.php"
        self.query_params = {"al": 1, "c[section]": "audio"}

    async def get_info(self, query: str) -> List[AudioSearchResult]:
        params = self.query_params.copy()
        params['c[q]'] = urllib.parse.quote_plus(query)
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url, params=params)
        data = await response.read()
        print(data)
        return []

    def get_by_api(self):
        vk_session = vk_api.vk_api.VkApi('login', 'password')
        vk_session.auth()
        print(f'my token = "{vk_session.token}"')
        print(vk_session)

        vk = vk_session.get_api()
        vkaudio = VkAudio(vk_session)
        print([x for x in vkaudio.search('sandstorm')])

        # session = vk.AuthSession('3380204', 'nextyear@list.ru', 'pr1s0nVK2', scope='friends')
        # vk_api = vk.API(session)
        # friends = vk_api.friends.get()
        pprint(vk.audio.search(q='sandstorm'))
