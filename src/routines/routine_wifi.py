import json
import pygame
import requests
import time
import pprint
import os
import requests
import textdistance
import random
import RPi.GPIO as GPIO


button_start = 16

led_start = 18

state_start = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_start, GPIO.OUT)

if __name__ == "__main__":
    while True:
        if not GPIO.input(button_start):
            if not temp_pressed:
                state_start = not state_start
                response = requests.post('https://battlemythe.net/api/anniv/2020/relay/34', json={"status": state_start})
                temp_pressed = True
        else:
            temp_pressed = False
        GPIO.output(led_start, state_start)
        time.sleep(0.016)