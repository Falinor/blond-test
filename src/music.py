from random import choice
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from cache import cache
from track import Track


auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


@cache.cache()
def playlists(category, limit=20, offset=0):
    return sp.category_playlists(
        category_id=category,
        country='FR',
        limit=limit,
        offset=offset
    )['playlists']['items']


def random_playlist(category, limit=20, offset=0):
    pls = playlists(category, limit, offset)
    # TODO: do not use the playlist if it has already been played
    return choice(pls)


@cache.cache()
def tracks(playlist, limit=20, offset=0):
    ts = [
        item['track']
        for item
        in sp.playlist_items(
            playlist_id=playlist['id'],
            market='FR',
            fields='items(track(name,artists(name)))',
            additional_types=['track'],
            limit=limit,
            offset=offset
        )['items']
    ]
    return [from_spotify_track(t) for t in ts]


def random_track(playlist, limit=20, offset=0):
    ts = tracks(playlist, limit, offset)
    return choice(ts)


def from_spotify_track(track):
    return Track(
        title=track['name'],
        artists=[artist['name'] for artist in track['artists']]
    )
