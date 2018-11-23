from __future__ import print_function
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3

stopwords = nltk.corpus.stopwords.words('english')

stemmer = SnowballStemmer("english")

df = pd.read_csv('tweets.csv', index_col=0)

df = df[:10000]


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(
        text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text)
              for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


totalvocab_stemmed = []
totalvocab_tokenized = []
for i in df['Text']:
    # for each item in 'synopses', tokenize/stem
    allwords_stemmed = tokenize_and_stem(i)
    # extend the 'totalvocab_stemmed' list
    totalvocab_stemmed.extend(allwords_stemmed)

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame(
    {'words': totalvocab_tokenized}, index=totalvocab_stemmed)
print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')


# define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=5.0, max_features=200000,
                                   min_df=0.1, stop_words='english',
                                   use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

# fit the vectorizer to synopses
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Text'])

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()

# print(terms)

dist = 1 - cosine_similarity(tfidf_matrix)

# print(dist[:20])


num_clusters = 5

km = KMeans(n_clusters=num_clusters)

km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

# joblib.dump(km,  'tweet_cluster.pkl')

tweets = {'TweetID': df.index.values,
          'Text': df['Text'], 'cluster': clusters, 'UserID': df['UserID']}

print(len(clusters), len(df.keys()))
frame = pd.DataFrame(tweets, index=[clusters], columns=[
                     'TweetID', 'Text', 'cluster', 'UserID'])

print(frame['cluster'].value_counts())


print("Top terms per cluster:")
print()
# sort cluster centers by proximity to centroid
order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')

    for ind in order_centroids[i, :10]:  # words to display per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[
              0][0].encode('utf-8', 'ignore'), end=',')
    print('\n\n')
