import plyvel
import pandas as pd
import bson

# pro to csv

proDB = plyvel.DB('./proTweets', create_if_missing=True)

proDF = pd.DataFrame(
    columns=['UserID', 'UserName', 'Text', 'NumberRT', 'Retweeters'])
for key, value in proDB:
    tweet = bson.loads(value)
    proDF.loc[int(key.decode('utf-8'))] = [tweet['user']['id_str'], tweet['user']
                                           ['screen_name'], tweet['text'], '', '']
proDB.close()

proTweetsIndices = proDF.index.tolist()

pro2DB = plyvel.DB('./pro2Tweets', create_if_missing=True)

for key, value in pro2DB:
    tweet = bson.loads(value)
    retweetedStatusID = tweet['retweeted_status']['id']
    userID = tweet['user']['id_str']
    if retweetedStatusID in proTweetsIndices:
        proDF.loc[retweetedStatusID]['Retweeters'] += userID + ','

pro2DB.close()

for index, row in proDF.iterrows():
    proDF.loc[index]['NumberRT'] = len(row['Retweeters'].split(',')) - 1

proDF.to_csv('pro.csv')

# anti to csv

antiDB = plyvel.DB('./antiTweets', create_if_missing=True)

antiDF = pd.DataFrame(
    columns=['UserID', 'UserName', 'Text', 'NumberRT', 'Retweeters'])
for key, value in antiDB:
    tweet = bson.loads(value)
    antiDF.loc[int(key.decode('utf-8'))] = [tweet['user']['id_str'],
                                            tweet['user']['screen_name'], tweet['text'], '', '']
antiDB.close()

antiTweetsIndices = antiDF.index.tolist()

anti2DB = plyvel.DB('./anti2Tweets', create_if_missing=True)

for key, value in anti2DB:
    tweet = bson.loads(value)
    retweetedStatusID = tweet['retweeted_status']['id']
    userID = tweet['user']['id_str']
    if retweetedStatusID in antiTweetsIndices:
        antiDF.loc[retweetedStatusID]['Retweeters'] += userID + ','

anti2DB.close()

for index, row in antiDF.iterrows():
    antiDF.loc[index]['NumberRT'] = len(row['Retweeters'].split(',')) - 1

antiDF.to_csv('anti.csv')
