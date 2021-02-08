from typing import List


class Track:
    def __init__(self, title: str, artists: List[str]):
        super().__init__()
        self.title = title
        self.artists = artists

    def encode(self):
        return {
            "title": self.title,
            "artists": self.artists[0]
        }
