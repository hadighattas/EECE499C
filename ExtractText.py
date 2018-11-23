import plyvel
import pandas as pd
import bson
import time

start_time = time.time()

count = 0

db = plyvel.DB('./tweets', create_if_missing=True)

df = pd.DataFrame(
    columns=['UserID', 'UserName', 'Text'])

for key, value in db:
    count = count + 1
    tweet = bson.loads(value)
    df.loc[int(key.decode('utf-8'))] = [tweet['user']['id_str'], tweet['user']
                                        ['screen_name'], tweet['text'].replace('\n', ' ').replace('\r', '')]
    if count == 10000:
        break

db.close()
df.to_csv('tweets.csv')

print("--- %s seconds ---" % (time.time() - start_time))
