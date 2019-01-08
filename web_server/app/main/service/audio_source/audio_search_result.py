from attr import dataclass


@dataclass
class AudioSearchResult():
    title: str
    duration: int
    url: str
