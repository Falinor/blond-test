import os.path
import pygame
import sys
import textdistance
import random
import RPi.GPIO as GPIO

import music
from player import Player
from categories import categories
from thread_http import *
from constants import *


# constantes d'affichage
res_x = 1920
res_y = 1080

# constantes du jeu en secondes
time_global = 5 * 60 # durée d'une partie
time_loading = 3 # temps de chargement entre les musiques
time_answer = 15 # temps maximal pour répondre
time_song = 30 # temps maximal d'une musique
time_end = 15 # temps sur l'écran "c'est fini"
time_scores = 0 # temps sur l'écran des scores

button_1 = 20
button_2 = 21
button_start = 16

led_1 = 24
led_2 = 23
led_start = 18

led_white = 6
led_red = 19
led_yellow = 13
led_all = 26

relay_1 = 8
relay_2 = 25

sounds = {}
screens = [None]
texts = [""]
fonts = {}

song = {}
musics = []

state_led = [0]

thread = ThreadHttp()

player = Player()

state = {
    "attraction": None,
    "ranking": [],
    "users": None,
    "state": LOBBY,
    "timerGet": 1,
    "current_music": 0,
    "timer_1": 0,
    "timer_2": 0,
    "player_1": 0,
    "player_2": 0,
    "passed_time": 0,
    "global_time": 0,
    "artiste": False,
    "titre": False,
    "has_buzzed_1": False,
    "has_buzzed_2": False,
    "has_won_1": False,
    "has_won_2": False,
    "index_rules": 0,
    "done": False,
    "category": None
}

end_0 = pygame.image.load(os.path.join("..", "data", "images", "end_0.png"))
end_0 = pygame.transform.scale(end_0, (res_x, res_y))
ranking = pygame.image.load("../data/images/ranking.png")
ranking = pygame.transform.scale(ranking, (res_x, res_y))
ranking_start = pygame.image.load("../data/images/ranking_start.png")
ranking_start = pygame.transform.scale(ranking_start, (res_x, res_y))
end_1 = pygame.image.load("../data/images/end_1.png")
end_1 = pygame.transform.scale(end_1, (res_x, res_y))
playing = pygame.image.load("../data/images/playing.png")
playing = pygame.transform.scale(playing, (res_x, res_y))
rules_2 = pygame.image.load("../data/images/rules_2.png")
rules_2 = pygame.transform.scale(rules_2, (res_x, res_y))
rules_0 = pygame.image.load("../data/images/rules_0.png")
rules_0 = pygame.transform.scale(rules_0, (res_x, res_y))
rules_1 = pygame.image.load("../data/images/rules_1.png")
rules_1 = pygame.transform.scale(rules_1, (res_x, res_y))
input_1 = pygame.image.load("../data/images/input_1.png")
input_1 = pygame.transform.scale(input_1, (res_x, res_y))
input_0 = pygame.image.load("../data/images/input_0.png")
input_0 = pygame.transform.scale(input_0, (res_x, res_y))
end_eq = pygame.image.load("../data/images/end_eq.png")
end_eq = pygame.transform.scale(end_eq, (res_x, res_y))
win_0 = pygame.image.load("../data/images/win_0.png")
win_0 = pygame.transform.scale(win_0, (res_x, res_y))
win_1 = pygame.image.load("../data/images/win_1.png")
win_1 = pygame.transform.scale(win_1, (res_x, res_y))
win_eq = pygame.image.load("../data/images/win_eq.png")
win_eq = pygame.transform.scale(win_eq, (res_x, res_y))
loose = pygame.image.load("../data/images/loose.png")
loose = pygame.transform.scale(loose, (res_x, res_y))
start = pygame.image.load("../data/images/start.png")
start = pygame.transform.scale(start, (res_x, res_y))
wrong_0 = pygame.image.load("../data/images/wrong_0.png")
wrong_0 = pygame.transform.scale(wrong_0, (res_x, res_y))
wrong_1 = pygame.image.load("../data/images/wrong_1.png")
wrong_1 = pygame.transform.scale(wrong_1, (res_x, res_y))

titre_ok = pygame.image.load("../data/images/titre_ok.png")
titre_nope = pygame.image.load("../data/images/titre_nope.png")
artiste_ok = pygame.image.load("../data/images/artiste_ok.png")
artiste_nope = pygame.image.load("../data/images/artiste_nope.png")


def set_attraction(a):
    state["attraction"] = a

def set_ranking(a):
    state["ranking"] = a

def set_users(users):
    state["users"] = users

def init():
    pygame.init()
    pygame.mixer.init()
    # screens[0] = pygame.display.set_mode((res_x, res_y), pygame.FULLSCREEN | pygame.HWSURFACE)
    screens[0] = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption("Blind test")
    sounds["buzz"] = pygame.mixer.Sound('./../data/buzzer.ogg')
    sounds["good"] = pygame.mixer.Sound('./../data/good.ogg')
    sounds["bad"] = pygame.mixer.Sound('./../data/bad.ogg')
    sounds["loose_0"] = []
    sounds["loose_1"] = []
    sounds["win_0"] = []
    sounds["win_1"] = []
    for i in range(9):
        sounds["loose_0"].append(pygame.mixer.Sound("./../data/bruitages/Loose_Monique_" + str(i + 1) + ".ogg"))
        sounds["loose_1"].append(pygame.mixer.Sound("./../data/bruitages/Loose_Véro_" + str(i + 1) + ".ogg"))
        sounds["win_0"].append(pygame.mixer.Sound("./../data/bruitages/Win_Monique_" + str(i + 1) + ".ogg"))
        sounds["win_1"].append(pygame.mixer.Sound("./../data/bruitages/Win_Véro_" + str(i + 1) + ".ogg"))
    sounds["final_0"] = pygame.mixer.Sound("./../data/bruitages/Final_Monique_Wins.ogg")
    sounds["final_1"] = pygame.mixer.Sound("./../data/bruitages/Final_Véro_Wins.ogg")
    sounds["final_eq"] = pygame.mixer.Sound("./../data/bruitages/Final_exaequo.ogg")
    pygame.font.init()
    fonts["normal"] = pygame.font.SysFont("Comis Sans MS", 30)
    fonts["normal_mais_un_peu_plus"] = pygame.font.SysFont("Comis Sans MS", 45)
    fonts["big"] = pygame.font.SysFont("Comis Sans MS", 80)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led_1, GPIO.OUT)
    GPIO.setup(led_2, GPIO.OUT)
    GPIO.setup(led_start, GPIO.OUT)
    GPIO.setup(led_white, GPIO.OUT)
    GPIO.setup(led_red, GPIO.OUT)
    GPIO.setup(led_yellow, GPIO.OUT)
    GPIO.setup(led_all, GPIO.OUT)
    GPIO.setup(relay_1, GPIO.OUT)
    GPIO.setup(relay_2, GPIO.OUT)
    light_remote_led("all")


def init_musics():
    state["category"] = random.choice(categories)
    playlist = music.random_playlist(category=state["category"])
    state["category"] = state["category"].capitalize()
    tracks = music.tracks(playlist)
    # TODO: check this out
    # music_service.tracks seems to be launched in a thread
    # which resolves after the loading completes, so the game
    # ends before it could be played
    musics.extend(tracks)


def fill_background(color):
    screen = screens[0]
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(color)
    screen.blit(background, (0, 0))


def get_next_music():
    track = musics[state["current_music"]]
    state["current_music"] += 1
    state["answer_titre"] = track.title
    # TODO: handle multiple artists
    state["answer_artiste"] = track.artists[0]
    state["has_won_1"] = False
    state["has_won_2"] = False
    player.enqueue(track)
    player.play()
    # WARNING: FAUT PAS FAIRE CA
    # player.set_volume(0.5)
    # pygame.mixer.music.load("./../data/musics/" + music)
    # pygame.mixer.music.play()
    # pygame.mixer.music.set_volume(0.5)


def update_remote_leds():
    if state_led[0] > 0:
        state_led[0] -= 1
        if state_led[0] == 0:
            GPIO.output(led_white, False)
            GPIO.output(led_red, False)
            GPIO.output(led_yellow, False)
            GPIO.output(led_all, False)


def light_remote_led(led):
    if led == "white":
        GPIO.output(led_white, True)
    elif led == "red":
        GPIO.output(led_red, True)
    elif led == "yellow":
        GPIO.output(led_yellow, True)
    elif led == "all":
        GPIO.output(led_all, True)
    state_led[0] = 5


def update():
    update_remote_leds()
    if (state["state"] == LOADING or state["state"] == MUSIC_PLAY) and (state["current_music"] > len(musics) or ("global_time" in state and state["global_time"] > 0 and time.time() - state["global_time"] > time_global)):
        state["time"] = time.time()
        pygame.mixer.music.stop()
        player.stop()
        state["state"] = END
    if state["state"] == LOBBY:
        update_lobby()
    elif state["state"] == REGLES:
        update_regles()
    elif state["state"] == LOADING:
        update_loading()
    elif state["state"] == MUSIC_PLAY:
        update_music_play()
    elif state["state"] == END:
        update_end()
    elif state["state"] == SCORES:
        update_scores()


def update_lobby():
    # Mode autonome
    state["player_1"] = {
        "userId": "id1",
        "username": "Monique",
        "points": 0
    }
    state["player_2"] = {
        "userId": "id2",
        "username": "Véro",
        "points": 0
    }
    led = False
    if state["player_1"] and state["player_2"]:
        led = True
    GPIO.output(led_start, led)
    if not GPIO.input(button_start) and state["player_1"] and state["player_2"]:
        state["state"] = REGLES
        state["index_rules"] = 0
        state["pressed"] = True
        light_remote_led("white")
        GPIO.output(led_start, True)
        GPIO.output(led_1, False)
        GPIO.output(led_2, False)


def update_regles():
    if GPIO.input(button_start):
        state["pressed"] = False
    elif not state["pressed"]:
        state["index_rules"] += 1
        if state["index_rules"] >= 3:
            init_musics()
            light_remote_led("white")
            GPIO.output(led_start, False)
            GPIO.output(led_1, False)
            GPIO.output(led_2, False)
            state["state"] = LOADING
            state["time"] = time.time()


def update_loading():
    s = int(4 * (time.time() - state["time"])) % 2
    GPIO.output(led_start, s)
    GPIO.output(led_1, s)
    GPIO.output(led_2, s)
    if not GPIO.input(button_start) or not player.is_playing():
        # if time.time() - state["time"] > time_loading:
        if state["current_music"] >= len(musics):
            state["time"] = time.time()
            player.stop()
            state["state"] = END
        else:
            state["state"] = MUSIC_PLAY
            state["time"] = time.time()
            state["global_time"] = time.time() - state["passed_time"]
            GPIO.output(led_start, False)
            GPIO.output(led_1, True)
            GPIO.output(led_2, True)
            get_next_music()
            light_remote_led("all")


def update_music_play():
    if not GPIO.input(button_1) and state["timer_1"] == 0 and state["timer_2"] == 0 and not state["has_buzzed_1"]:
        sounds["buzz"].play()
        light_remote_led("red")
        texts[0] = ""
        player.pause()
        state["timer_1"] = time.time()
        state["has_buzzed_1"] = True
        GPIO.output(led_1, True)
        GPIO.output(led_2, False)
        GPIO.output(relay_1, True)
    if state["timer_1"] > 0 and time.time() - state["timer_1"] > time_answer:
        sounds["bad"].play()
        GPIO.output(relay_1, False)
        sounds["loose_0"][random.randint(0, 8)].play()
        light_remote_led("all")
        texts[0] = ""
        GPIO.output(led_1, False)
        state["timer_1"] = 0
        state["time"] += time_answer
        player.play()
        # pygame.mixer.music.set_volume(0.5)
        GPIO.output(led_1, not state["has_buzzed_1"])
        GPIO.output(led_2, not state["has_buzzed_2"])
    if not GPIO.input(button_2) and state["timer_2"] == 0 and state["timer_1"] == 0 and not state["has_buzzed_2"]:
        sounds["buzz"].play()
        light_remote_led("yellow")
        texts[0] = ""
        state["has_buzzed_2"] = True
        player.pause()
        state["timer_2"] = time.time()
        GPIO.output(led_1, False)
        GPIO.output(led_2, True)
        GPIO.output(relay_2, True)
    if state["timer_2"] > 0 and time.time() - state["timer_2"] > time_answer:
        sounds["bad"].play()
        sounds["loose_1"][random.randint(0, 8)].play()
        light_remote_led("all")
        texts[0] = ""
        state["timer_2"] = 0
        state["time"] += time_answer
        GPIO.output(led_1, not state["has_buzzed_1"])
        GPIO.output(led_2, not state["has_buzzed_2"])
        GPIO.output(relay_2, False)
        player.play()
        # pygame.mixer.music.set_volume(0.5)
    if (state["artiste"] and state["titre"]) or ((state["timer_1"] == 0 and state["timer_2"] == 0) and (
            (state["artiste"] and state["titre"]) or time.time() - state["time"] > time_song)) or (
                (state["timer_1"] == 0 and state["timer_2"] == 0) and state["has_buzzed_1"] and state["has_buzzed_2"]):
        player.play()
        GPIO.output(relay_1, False)
        GPIO.output(relay_2, False)
        # pygame.mixer.music.set_volume(0.2)
        light_remote_led("white")
        state["passed_time"] += time.time() - (state["global_time"] + state["passed_time"])
        state["state"] = LOADING
        state["timer_1"] = 0
        state["timer_2"] = 0
        state["has_buzzed_1"] = False
        state["has_buzzed_2"] = False
        state["titre"] = False
        state["artiste"] = False
        state["time"] = time.time()
        if state["has_won_1"] and state["has_won_2"]:
            sounds["final_eq"].play()
        elif state["has_won_1"]:
            sounds["win_0"][random.randint(0, 8)].play()
        elif state["has_won_2"]:
            sounds["win_1"][random.randint(0, 8)].play()
        else:
            if random.random() > 0.5:
                sounds["loose_0"][random.randint(0, 8)].play()
            else:
                sounds["loose_1"][random.randint(0, 8)].play()
    if state["timer_1"] > 0 or state["timer_2"] > 0:
        if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
            texts[0] = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state["done"] = True
        if event.type == pygame.KEYDOWN:
            if state["timer_1"] > 0 or state["timer_2"] > 0:
                if event.key == pygame.K_BACKSPACE:
                    texts[0] = texts[0][:-1]
                elif event.key == pygame.K_RETURN:
                    if check_match(texts[0], state["answer_titre"]) and not state["titre"]:
                        sounds["good"].play()
                        state["titre"] = True
                        if state["timer_1"]:
                            state["player_1"]["points"] += 1
                            state["has_won_1"] = True
                        else:
                            state["player_2"]["points"] += 1
                            state["has_won_2"] = True
                        texts[0] = ""
                        state["timer_1" if state["timer_1"] else "timer_2"] = time.time()
                    if check_match(texts[0], state["answer_artiste"]) and not state["artiste"]:
                        sounds["good"].play()
                        if state["timer_1"]:
                            state["player_1"]["points"] += 1
                            state["has_won_1"] = True
                        else:
                            state["player_2"]["points"] += 1
                            state["has_won_2"] = True
                        texts[0] = ""
                        state["artiste"] = True
                        state["timer_1" if state["timer_1"] else "timer_2"] = time.time()
                else:
                    texts[0] += event.unicode if event.unicode in "abcdefghijklimonpqrstuvwxyz01234567890!.,- " else ""


def check_match(s1, s2):
    charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
    t1 = "".join([a for a in s1.lower() if a in charset]).lower()
    t2 = "".join([a for a in s2.lower() if a in charset]).lower()
    return textdistance.levenshtein(t1, t2) <= 3


def update_end():
    if time.time() - state["time"] > time_end:
        state["time"] = time.time()
        state["state"] = LOBBY
        state["timerGet"] = 1
        state["current_music"] = 0
        state["passed_time"] = 0
        state["global_time"] = 0
        state["timer_1"] = 0
        state["timer_2"] = 0
        state["player_1"] = None
        state["player_2"] = None
        state["artiste"] = False
        state["titre"] = False
        state["has_buzzed_1"] = False
        state["has_buzzed_2"] = False
        state["done"] = 0


def update_scores():
    if time.time() - state["time"] > time_scores:
        state["state"] = LOBBY
        state["time"] = time.time()
        state["timerGet"] = 1
        state["current_music"] = 0
        state["global_time"] = 0
        state["passed_time"] = 0
        state["timer_1"] = 0
        state["timer_2"] = 0
        state["player_1"] = None
        state["player_2"] = None
        state["artiste"] = False
        state["titre"] = False
        state["has_buzzed_1"] = False
        state["has_buzzed_2"] = False
        state["done"] = 0

def render():
    fill_background((255, 255, 255))
    if state["state"] == LOBBY:
        render_lobby()
    elif state["state"] == LOADING:
        render_loading()
    elif state["state"] == MUSIC_PLAY:
        render_music_playing()
    elif state["state"] == SCORES:
        render_ranking()
        render_scores()
    elif state["state"] == REGLES:
        render_rules()
    elif state["state"] == END:
        render_end()
    else:
        render_default()
    pygame.display.flip()


def render_lobby():
    screen = screens[0]
    if state["player_1"] and state["player_2"]:
        screen.blit(ranking_start, (0, 0))
    else:
        screen.blit(ranking, (0, 0))
    player_1 = state["player_1"]
    text = player_1["username"] if player_1 else "NO USER YET"
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (res_x * 0.153 - w/2, res_y * 2 / 3 - h / 2))
    player_2 = state["player_2"]
    text = player_2["username"] if player_2 else "NO USER YET"
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (res_x * 0.622 - w/2, res_y * 2 / 3 - h / 2))
    render_ranking()


def render_rules():
    screen = screens[0]
    if state["index_rules"] == 0:
        screen.blit(rules_0, (0, 0))
    elif state["index_rules"] == 1:
        screen.blit(rules_1, (0, 0))
    else:
        screen.blit(rules_2, (0, 0))


def render_end():
    screen = screens[0]
    if state["player_1"]["points"] > state["player_2"]["points"]:
        screen.blit(end_0, (0, 0))
    elif state["player_1"]["points"] < state["player_2"]["points"]:
        screen.blit(end_1, (0, 0))
    else:
        screen.blit(end_eq, (0, 0))
    text = state["player_1"]["username"]
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (res_x * 0.153 - w / 2, res_y * 0.71 - h / 2))
    text = str(state["player_1"]["points"])
    surface_text = fonts["big"].render(text, False, (0, 255, 0))
    w, h = fonts["big"].size(text)
    screen.blit(surface_text, (res_x * 0.153 - w / 2, res_y * 0.77 - h / 2))
    text = state["player_2"]["username"]
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (res_x * 0.622 - w / 2, res_y * 0.71 - h / 2))
    text = str(state["player_2"]["points"])
    surface_text = fonts["big"].render(text, False, (0, 255, 0))
    w, h = fonts["big"].size(text)
    screen.blit(surface_text, (res_x * 0.622 - w / 2, res_y * 0.77 - h / 2))
    text = "C'est terminé !"
    surface_text = fonts["big"].render(text, False, (0, 255, 0))
    w, h = fonts["big"].size(text)
    screen.blit(surface_text, (res_x * 0.385 - w / 2, res_y * 0.73 - h / 2))



def render_scores():
    screen = screens[0]
    text = str(state["player_1"]["points"]) + " pts"
    surface_text = fonts["big"].render(text, False, (0, 0, 0))
    w, h = fonts["big"].size(str(text))
    screen.blit(surface_text, (res_x / 6 - w / 2, 3 * h))
    text = str(state["player_2"]["points"]) + " pts"
    surface_text = fonts["big"].render(text, False, (0, 0, 0))
    w, h = fonts["big"].size(str(text))
    screen.blit(surface_text, (res_x * 5/ 6 - w / 2, 3 * h))


def render_loading():
    screen = screens[0]
    if state["current_music"] > 0:
        if state["has_won_1"] and state["has_won_2"]:
            screen.blit(win_eq, (0, 0))
        elif state["has_won_1"]:
            screen.blit(win_0, (0, 0))
        elif state["has_won_2"]:
            screen.blit(win_1, (0, 0))
        else:
            screen.blit(loose, (0, 0))
    else:
        screen.blit(start, (0, 0))

    if state["current_music"] > 0:
        # Display title
        title = f'Titre : {state["answer_titre"]}'
        surface_text = fonts["normal_mais_un_peu_plus"].render(title, False, (0, 255, 0))
        screen.blit(surface_text, (res_x / 4, res_y * 0.7))
        # Display artist
        artist = f'Artiste : {state["answer_artiste"]}'
        surface_text = fonts["normal_mais_un_peu_plus"].render(artist, False, (0, 255, 0))
        screen.blit(surface_text, (res_x / 4, res_y * 0.74))
        # Display skip text
        skip = "Appuyez sur le bouton start pour passer"
        surface_text = fonts["normal"].render(skip, False, (0, 255, 255))
        screen.blit(surface_text, (res_x / 4, res_y * 0.8))
    else:
        seconds = time_loading - int(time.time() - state["time"])
        surface_text = fonts["big"].render(str(seconds), False, (255, 255, 255))
        w, h = fonts["big"].size(str(seconds))
        screen.blit(surface_text, (res_x * 0.36 - w/2, res_y * 0.48 - h / 2))


def render_music_playing():
    screen = screens[0]
    render_scores()
    if state["timer_1"] == 0 and state["timer_2"] == 0:
        # music playing
        screen.blit(playing, (0, 0))
        render_loading_bar(time.time() - state["time"], time_song)
        gt = time_global - (time.time() - state["global_time"])
        minutes = int(gt / 60)
        secondes = int(gt - 60 * minutes)
        text = ("0" if minutes < 10 else "") + str(minutes) + ":" + ("0" if secondes < 10 else "") + str(secondes)
        surface_text = fonts["big"].render(text, False, (255, 255, 255))
        w, h = fonts["big"].size(text)
        screen.blit(surface_text, (res_x * 0.51 - w/2, res_y * 0.55))

        # Display the music category
        surface_text = fonts["normal_mais_un_peu_plus"].render(state["category"], False, (0, 0, 255))
        w, h = fonts["normal_mais_un_peu_plus"].size(state["category"])
        screen.blit(surface_text, (res_x * 0.5 - w / 2, res_y * 0.9))

    elif state["timer_1"] > 0:
        # player 1 answering
        screen.blit(input_0, (0, 0))
        text = state["player_1"]["username"] + " a buzzé"
        surface_text = fonts["normal"].render(text, False, (255, 255, 255))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (res_x * 0.43 - w/2, res_y * 0.45 - h / 2))
        text = texts[0]
        surface_text = fonts["normal_mais_un_peu_plus"].render(text, False, (0, 0, 0))
        w, h = fonts["normal_mais_un_peu_plus"].size(text)
        screen.blit(surface_text, (res_x * 0.43 - w/2, res_y * 0.61 - h / 2))
        render_loading_bar_answer(time.time() - state["timer_1"], time_answer)
        text = "Trouve l'artiste ou le titre"
        if state["artiste"]:
            text = "Trouve le titre"
        elif state["titre"]:
            text = "Trouve l'artiste"
        surface_text = fonts["normal"].render(text, False, (255, 255, 255))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (res_x *0.43 - w/2, res_y *0.50 - h / 2))
        x_artiste = 0.18
        x_titre = 0.43
        y_both = 0.21
        if state["artiste"]:
            screen.blit(artiste_ok, (res_x * x_artiste, res_y * y_both))
        else:
            screen.blit(artiste_nope, (res_x * x_artiste, res_y * y_both))
        if state["titre"]:
            screen.blit(titre_ok, (res_x * x_titre, res_y * y_both))
        else:
            screen.blit(titre_nope, (res_x * x_titre, res_y * y_both))

    elif state["timer_2"] > 0:
        # player 2 answering
        screen.blit(input_1, (0, 0))
        text = state["player_2"]["username"] + " a buzzé"
        surface_text = fonts["normal"].render(text, False, (0, 0, 0))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (res_x *0.43 - w/2, res_y *0.45 - h / 2))
        text = texts[0]
        surface_text = fonts["normal_mais_un_peu_plus"].render(text, False, (0, 0, 0))
        w, h = fonts["normal_mais_un_peu_plus"].size(text)
        screen.blit(surface_text, (res_x *0.43 - w/2, res_y *0.61 - h / 2))
        render_loading_bar_answer(time.time() - state["timer_2"], time_answer)
        text = "Trouve l'artiste ou le titre"
        if state["artiste"]:
            text = "Trouve le titre"
        elif state["titre"]:
            text = "Trouve l'artiste"
        x_artiste = 0.18
        x_titre = 0.43
        y_both = 0.21
        if state["artiste"]:
            screen.blit(artiste_ok, (res_x * x_artiste, res_y * y_both))
        else:
            screen.blit(artiste_nope, (res_x * x_artiste, res_y * y_both))
        if state["titre"]:
            screen.blit(titre_ok, (res_x * x_titre, res_y * y_both))
        else:
            screen.blit(titre_nope, (res_x * x_titre, res_y * y_both))
        surface_text = fonts["normal"].render(text, False, (255, 255, 255))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (res_x *0.43 - w/2, res_y *0.50 - h / 2))


def render_loading_bar(current, total):
    screen = screens[0]
    w = res_x * 0.73
    background = pygame.Surface((w * current / total, 20))
    background = background.convert()
    background.fill((0, 0, 255))
    screen.blit(background, (res_x / 2 - w / 2, res_y * 0.32))


def render_loading_bar_answer(current, total):
    screen = screens[0]
    w = res_x * 0.41
    background = pygame.Surface((w * current / total, 20))
    background = background.convert()
    background.fill((255, 255, 255))
    screen.blit(background, (res_x * 0.15, res_y * 0.81))


def render_default():
    screen = screens[0]
    text = state["state"]
    surface_text = fonts["normal"].render(text, False, (0, 0, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (res_x / 2 - w/2, res_y / 2 - h / 2))


def render_ranking():
    if not len(state["ranking"]):
        return
    screen = screens[0]
    size_x = res_x * 0.25
    size_y = res_y * 0.35
    start_x = res_x * 0.27
    start_y = res_y / 3
    step_y = size_y / (1 + len(state["ranking"]))
    text = "Player"
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (start_x, start_y + step_y /2 - h))
    text = "Pts"
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (start_x + size_x * 2 / 3, start_y + step_y /2 - h))
    text = "#"
    surface_text = fonts["normal"].render(text, False, (0, 255, 0))
    w, h = fonts["normal"].size(text)
    screen.blit(surface_text, (start_x + size_x - w - 15, start_y + step_y /2 - h))
    i = 1
    for rank in state["ranking"]:
        text = rank["username"]
        surface_text = fonts["normal"].render(text, False, (0, 255, 0))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (start_x, start_y + (2 * i + 1) * step_y /2 - h / 2))
        text = str(rank["points"])
        surface_text = fonts["normal"].render(text, False, (0, 255, 0))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (start_x + size_x * 2 / 3, start_y + (2 * i + 1) * step_y /2 - h / 2))
        text = str(rank["rank"])
        surface_text = fonts["normal"].render(text, False, (0, 255, 0))
        w, h = fonts["normal"].size(text)
        screen.blit(surface_text, (start_x + size_x - w - 15, start_y + (2 * i + 1) * step_y /2 - h / 2))
        i += 1


if __name__ == "__main__":
    init()
    GPIO.output(led_1, False)
    GPIO.output(led_2, False)
    try:
        if True:
            state["done"] = False
            while not state["done"]:
                update()
                render()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        thread.stop()
        player.stop()
        pygame.quit()
        GPIO.cleanup()
        sys.exit()
