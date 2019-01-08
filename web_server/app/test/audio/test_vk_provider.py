import asyncio

from app.main.service.audio_source.vk_provider import VkProvider
from app.test.base import BaseTestCase


class TestVkProvider(BaseTestCase):

    def test_query_request(self):
        provider = VkProvider("token")
        query = "An deiner Seite"
        # loop = asyncio.get_event_loop()
        # search_results = loop.run_until_complete(provider.get_info(query))
        # print(search_results)
        provider.get_by_api()