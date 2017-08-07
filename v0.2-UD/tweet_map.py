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

        self.user_map = Basemap(
            projection='merc',
            llcrnrlat=-80,
            urcrnrlat=80,
            llcrnrlon=-180,
            urcrnrlon=180,
            lat_ts=20,
            resolution='c')
        self.user_map.drawcoastlines()
        self.user_map.fillcontinents(color='coral', lake_color='aqua')
        self.user_map.drawmapboundary(fill_color='aqua')
        plt.ion()
        plt.title("Users tweets about " + ''.join(query))
        plt.show()

    def on_data(self, data):
        tweet = MyTweet(data)
        print(tweet.tweet['coordinates'])
        if tweet.tweet['coordinates']:
            print(tweet.tweet['coordinates'])
            coordinates = tweet.tweet['coordinates']['coordinates']
            x, y = self.user_map(*coordinates)
            self.user_map.plot(
                x, y,
                marker='o',
                color='yellow',
                markeredgecolor='k',
                markersize=12)
            plt.draw()
            plt.pause(0.01)
        return True


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    query = [args.query]
    auth = twitter_client.get_twitter_auth()
    stream = Stream(auth, MyListener(query), async=True)
    stream.filter(track=query)
