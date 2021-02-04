from random import choice
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from categories import categories
from track import Track


class MusicService:
    def __init__(self) -> None:
        auth_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def random_playlist(self, category, limit=20, offset=0):
        playlists = self.sp.category_playlists(
            category_id=category,
            country='FR',
            limit=limit,
            offset=offset
        )['playlists']['items']
        # TODO: do not use the playlist if it has already been played
        return choice(playlists)

    def tracks(self, playlist, limit=20, offset=0):
        tracks = [
            item['track']
            for item
            in self.sp.playlist_items(
                playlist_id=playlist['id'],
                market='FR',
                fields='items(track(name,artists(name)))',
                additional_types=['track'],
                limit=limit,
                offset=offset
            )['items']
        ]
        return [from_spotify_track(t) for t in tracks]

    def random_track(self, playlist, limit=20, offset=0):
        tracks = [
            item['track']
            for item
            in self.sp.playlist_items(
                playlist_id=playlist['id'],
                market='FR',
                fields='items(track(name,artists(name)))',
                additional_types=['track'],
                limit=limit,
                offset=offset
            )['items']
        ]
        return from_spotify_track(choice(tracks))


def from_spotify_track(track: Track):
    return Track(
        title=track['name'],
        artists=[artist['name'] for artist in track['artists']]
    )


if __name__ == '__main__':
    service = MusicService()
    p = service.random_playlist('french_variety')
    track = service.random_track(p)
    print(track.title, track.artists)
