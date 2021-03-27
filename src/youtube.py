from os import environ as env
from typing import List
import googleapiclient.discovery

import random
from cache import cache, client


youtube = googleapiclient.discovery.build(
    'youtube',
    'v3',
    developerKey=env.get('YOUTUBE_API_KEY')
)


@cache.cache()
def search(title: str, artists: List[str]):
    try:
        result = youtube.search().list(
            q=f"{title} {','.join(artists)} lyrics",
            part='snippet',
            maxResults=1,
            regionCode='fr',
            type='video',
            fields='items(id(videoId))'
        ).execute()
        return result['items'][0]['id']['videoId']
    except:
        print('YouTube quota exceeded')
        # TODO: refactor this quick'n'dirty version
        # Return a random song from the cache
        keys = client.keys('rc:youtube.search:*')
        return client.get(random.choice(keys))
