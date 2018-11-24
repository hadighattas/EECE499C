import argparse
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
import plyvel
import bson
import matplotlib.pyplot as plt
import time

parser = argparse.ArgumentParser()
parser.add_argument('number_tweets', help='Max number of Tweets')
args = parser.parse_args()

numberOfTweets = int(args.number_tweets)

start_time = time.time()

G = nx.Graph()

proDB = plyvel.DB('./proTweets')
# pro2DB = plyvel.DB('./pro2Tweets')
antiDB = plyvel.DB('./antiTweets')
# anti2DB = plyvel.DB('./anti2Tweets')
dbs = [proDB, antiDB]
count = 0
blue_edges = []
green_edges = []
white_edges = [edge for edge in G.edges() if edge not in blue_edges]

print(numberOfTweets)
for db in dbs:
    count = 0
    for key, value in db:
        tweet = bson.loads(value)
        tweetID = key.decode("utf-8")
        userID = tweet['user']['id_str']
        count = count + 1
        try:
            retweetedSatusID = tweet['retweeted_status']['id_str']
            retweetedUserID = tweet['retweeted_status']['user']['id_str']
            if db.get(retweetedSatusID.encode()) != None:
                G.add_edge(userID, retweetedUserID)
                blue_edges.append((userID, retweetedUserID))
        except Exception as e:
            # print(e)
            pass

        try:
            replySatusID = tweet['in_reply_to_status_id_str']
            replyUserID = tweet['in_reply_to_user_id_str']
            if db.get(replySatusID.encode()) != None:
                G.add_edge(userID, replyUserID)
                green_edges.append((userID, replyUserID))
        except Exception as e:
            # print(e)
            pass

        if count == numberOfTweets:
            break

val_map = {}

for n, d in G.nodes(data=True):
    numberOfNeighbors = len(G[n].keys())
    if numberOfNeighbors == 1:
        val_map[n] = 1
    elif numberOfNeighbors in range(2, 6):
        val_map[n] = 5
    elif numberOfNeighbors in range(6, 25):
        val_map[n] = 10
    elif numberOfNeighbors > 24:
        val_map[n] = 15


values = [val_map.get(node, 0.25) for node in G.nodes()]

edge_colours = ['green' if not edge in blue_edges else 'blue'
                for edge in G.edges()]

pos = nx.spring_layout(G)
# for p in pos:  # raise text positions
#     pos[p][1] += 0.07

nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                       node_color=values, node_size=values)
# nx.draw_networkx_labels(G, pos, font_size=10)
nx.draw_networkx_edges(G, pos, edgelist=blue_edges,
                       edge_color='b')
nx.draw_networkx_edges(G, pos, edgelist=green_edges, edge_color='g')

print("--- %s seconds ---" % (time.time() - start_time))

plt.show()
