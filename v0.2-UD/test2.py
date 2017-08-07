from tweepy import Stream
from tweepy.streaming import StreamListener
from mpl_toolkits.basemap import Basemap
import time
import argparse
import twitter_client
import json
import string
import numpy as np
import matplotlib.pyplot as plt


from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

punctuation = list(string.punctuation)


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Capturer")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser


class MyTweet():

    def __init__(self, data):
        try:
            self.tweet = json.loads(data)
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)

    def tokenize(self):
        tknz = TweetTokenizer()
        terms = tknz.tokenize(self.tweet['text'])
        return terms

    def terms_filter(self, terms, strainer='only'):
        if strainer == 'only':
            terms_filtered = [
                term for term in terms if term not in stopwords and
                term not in punctuation and
                not term.startswith(('@', '#', 'https')) and
                not term.lower() == query.lower()]
        else:
            terms_filtered = terms
        return terms_filtered


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, query):
        self.query = query

    def on_data(self, data):
        tweet = MyTweet(data)
        if tweet.tweet['coordinates']:
            print(tweet.tweet['coordinates'])
        return True


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    query = [args.query]
    auth = twitter_client.get_twitter_auth()
    stream = Stream(auth, MyListener(query))
    stream.filter(track=query)












