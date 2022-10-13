from os import environ as env
from typing import List
import googleapiclient.discovery

from cache import cache


youtube = googleapiclient.discovery.build(
    "youtube",
    "v3",
    developerKey=env.get('YOUTUBE_API_KEY')
)


@cache.cache()
def search(title: str, artists: List[str]):
    print(f"Search for {title} by {artists}")
    result = youtube.search().list(
        q=f"{title} {','.join(artists)} lyrics",
        part='snippet',
        maxResults=1,
        regionCode="fr",
        type="video",
        fields='items(id(videoId))'
    ).execute()
    print('Found video', result['items'][0]['id']['videoId'])
    return result['items'][0]['id']['videoId']
