import plyvel

proDB = plyvel.DB('./proTweets', create_if_missing=True)
antiDB = plyvel.DB('./antiTweets', create_if_missing=True)
pro2DB = plyvel.DB('./pro2Tweets', create_if_missing=True)
anti2DB = plyvel.DB('./anti2Tweets', create_if_missing=True)

print('Number of pro tweets collected:', sum(1 for _ in proDB))
print('Number of pro2 tweets collected:', sum(1 for _ in pro2DB))

print('Number of anti tweets collected:', sum(1 for _ in antiDB))
print('Number of anti2 tweets collected:', sum(1 for _ in anti2DB))
