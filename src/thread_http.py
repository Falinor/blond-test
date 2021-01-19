import threading
import requests
import time
import pprint
from constants import *

GET = "GET"
POST = "POST"


class CallHttp:

    def __init__(self, method, endpoint, body, callback):
        self.method = method
        self.endpoint = endpoint
        self.body = body
        self.callback = callback


running = [True]


class ThreadHttp:

    def __init__(self):
        self.thread = None
        self.queue = []
        self.start_thread()

    def start_thread(self):
        self.thread = threading.Thread(target=self.http_function)
        self.thread.start()

    def call(self, element):
        self.queue.append(element)

    def http_function(self):
        while running[0]:
            if len(self.queue):
                element = self.queue.pop(0)
                try:
                    if element.method == GET:
                        r = requests.get(api_url + element.endpoint)
                        element.callback(r)
                    elif element.method == POST:
                        print(element.body)
                        r = requests.post(api_url + element.endpoint, json=element.body)
                        print("response to post")
                        print(r)
                        print(r.text)
                        element.callback(r)
                except Exception as e:
                    print(e)
            time.sleep(0.1)

    def stop(self):
        running[0] = False


