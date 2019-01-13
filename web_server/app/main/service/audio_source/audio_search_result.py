from attr import dataclass


@dataclass
class AudioSearchResult():
    title: str
    artist: str
    duration: int
    external_id: str
    url: str
