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
from pro import *

PRO_USERS = PRO_USERS_TOP_2000 + PRO_USERS_RANDOM_3000

# Connecting to database
proDB = plyvel.DB('./proTweets', create_if_missing=True)
pro2DB = plyvel.DB('./pro2Tweets', create_if_missing=True)

# Instantiating API class

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Callback function for the listener

count = 0


def processResponse(response):
    global count
    if response['type'] == 'data':
        try:
            count = count + 1
            data = response['data']
            tweetID = data['id']
            userID = data['user']['id_str']

            try:
                retweetUserID = data['retweeted_status']['user']['id_str']
            except:
                retweetUserID = ''

            if userID in PRO_USERS:
                proDB.put(str(tweetID).encode(), bson.dumps(data))
                print(count, 'Collected pro tweet with id:',
                      tweetID, 'from user:', userID)
            elif retweetUserID in PRO_USERS:
                pro2DB.put(str(tweetID).encode(), bson.dumps(data))
                print(count, 'Collected pro2 tweet with id:', tweetID,
                      'retweeted by:', userID, 'from user:', retweetUserID)

        except Exception as e:
            print('Error:', str(e))

    elif response['type'] == 'error':
        print('Error from API:', response['status'])


myStreamListener = Listener(processResponse)
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(follow=PRO_USERS, is_async=True)
