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


button_1 = 20
button_2 = 21
button_start = 16

led_1 = 24
led_2 = 23
led_start = 18

state_1 = True
state_2 = True
state_start = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_start, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)
GPIO.setup(led_start, GPIO.OUT)

if __name__ == "__main__":
    while True:
        if not GPIO.input(button_1):
            if not temp_pressed:
                state_1 = not state_1
                temp_pressed = True
        elif not GPIO.input(button_2):
            if not temp_pressed:
                state_2 = not state_2
                temp_pressed = True
        elif not GPIO.input(button_start):
            if not temp_pressed:
                state_start = not state_start
                temp_pressed = True
        else:
            temp_pressed = False
        GPIO.output(led_1, state_1)
        GPIO.output(led_2, state_2)
        GPIO.output(led_start, state_start)
        time.sleep(0.016)
