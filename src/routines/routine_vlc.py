import pafy
import vlc
import time


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=btPJPFnesV4"
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    while True:
        time.sleep(0.1)
