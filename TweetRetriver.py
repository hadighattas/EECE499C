# coding: utf-8

# # Retrieving Tweeets Stream API

# Importing libraries
import tweepy
import plyvel
import bson
import json

# Local imports
from StreamListener import Listener
from keys import *

# Connecting to database
db = plyvel.DB('./tweets', create_if_missing=True)

# Importing Twitter API keys and instantiating API class

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Defining keywords

keywords = [
    'Abrams',
    'Kemp',
    'Georgia Midterm',
    'Georgia Elections',
    'Republican Georgia',
    'Democrat Georgia',
]

# Callback function for the listener

count = 0


def processResponse(response):
    global count
    if response['type'] == 'data':
        count = count + 1
        data = response['data']
        id = data['id']
        print(count, 'Collected tweet with id:', id)
        db.put(str(id).encode(), bson.dumps(data))
    elif response['type'] == 'error':
        print(response['status'])


myStreamListener = Listener(processResponse)
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=keywords, is_async=True)
