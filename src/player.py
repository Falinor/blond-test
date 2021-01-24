import pafy
import vlc

import time
from music import MusicService
from track import Track
from youtube import YoutubeService


class Player:
    def __init__(self):
        self.track = None
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.youtube = YoutubeService()

    def enqueue(self, track: Track) -> None:
        url = self.youtube.search(track)
        audio = pafy.new(url).getbestaudio()
        media = self.instance.media_new(audio.url)
        self.player.set_media(media)

    def dequeue(self):
        pass

    def next(self):
        pass

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, volume: float):
        self.player.set_volume(volume * 100)


if __name__ == '__main__':
    music_service = MusicService()
    playlist = music_service.random_playlist('pop')
    track = music_service.random_track(playlist)
    player = Player()
    player.enqueue(track)
    player.play()
    print(track.title, track.artists)
    time.sleep(30)
