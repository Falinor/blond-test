from os import environ as env
import googleapiclient.discovery

from cache import cache
from track import Track


class YoutubeService:
    def __init__(self):
        self.youtube = googleapiclient.discovery.build(
            "youtube",
            "v3",
            developerKey=env.get('YOUTUBE_API_KEY')
        )

    @cache.cache()
    def search(self, track: Track):
        result = self.youtube.search().list(
            q=f"{track.title} {','.join(track.artists)} audio",
            part='snippet',
            maxResults=1,
            regionCode="fr",
            type="video",
            fields='items(id(videoId))'
        ).execute()
        return result['items'][0]['id']['videoId']
