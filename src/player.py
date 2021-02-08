import pafy
import vlc

from track import Track
import youtube


class Player:
    def __init__(self):
        self.track = None
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def enqueue(self, track: Track) -> None:
        url = youtube.search(title=track.title, artists=track.artists)
        audio = pafy.new(url).getbestaudio()
        media = self.instance.media_new(audio.url)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def is_playing(self):
        return True if self.player.is_playing() == 1 else False

    def stop(self):
        self.player.stop()

    def set_volume(self, volume: float):
        self.player.set_volume(volume * 100)
