import asyncio
import unittest

from app.main.service import track_service
from app.test.base import BaseTestCase


class TestTrackService(BaseTestCase):
    def test_upload_file(self):
        track = self.create_track('darude', 'sandstrom (remix)', 200, '123',
                                  "https://cs4-6v4.vkuseraudio.net/p16/2ea96b8581c61e.mp3?extra=WhyiszUEKLfPv9hk-uLIqpMtzOLfYDnMZyEg-o3euCKoZy4AFDtErgnh6seDxKeoGuDfTQeqF5TAjAWEl1CCHXw9D5QJ9vKSPzRIK7feboPDUeZC0nTC_IfkkB4WNGvzFLE1ZLHQmueI6U7F49QfiI6y")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            track_service.download_track(track)
        )


if __name__ == '__main__':
    unittest.main()
