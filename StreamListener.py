import tweepy
import json


class Listener(tweepy.StreamListener):
    callback = 0

    def __init__(self, callback):
        super()
        self.callback = callback

    def on_data(self, data):
        response = {
            'type': 'data',
            'data': json.loads(data)
        }
        self.callback(response)
        return(True)

    def on_error(self, status):
        response = {
            'type': 'error',
            'status': status
        }
        self.callback(response)
