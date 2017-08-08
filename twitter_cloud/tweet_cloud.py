from os import path
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import argparse
import string
import twitter_client
import json
import numpy as np

import matplotlib.pyplot as plt

from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from PIL import Image


punctuation = list(string.punctuation) + ['…', '...', ',']
stopwords = list(STOPWORDS) + \
    stopwords.words('english') + stopwords.words('french') + \
    ['RT', 'rt', 'via']

d = path.dirname(__file__)

image = np.array(Image.open(path.join(d, 'twitter.png')))
image_colors = ImageColorGenerator(image)
image_mask = np.array(Image.open(path.join(d, 'twitter_mask.png')))
font_path = path.join(
    path.dirname(path.dirname(path.abspath(__file__))),
    'fonts', 'OpenSansEmoji', 'OpenSansEmoji.ttf')


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
                not any([term.lower() == x.lower() for x in query])]
        else:
            terms_filtered = terms
        return terms_filtered


counter = Counter()


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, query):
        self.query = query

    def on_data(self, data):
        tweet = MyTweet(data)
        terms_only = tweet.terms_filter(tweet.tokenize(), 'only')
        counter.update(terms_only)
        print(counter)
        return True


def get_wordcloud():
    words = dict(counter.most_common(30))
    wordcloud = WordCloud(
        background_color='white',
        font_path=font_path,
        mask=image_mask,
        stopwords=stopwords+punctuation,
    ).generate_from_frequencies(words)
    return wordcloud


def display_wordcloud():
    wordcloud = get_wordcloud()
    plt.imshow(
        wordcloud.recolor(color_func=image_colors),
        interpolation='bilinear'
    )
    plt.axis('off')
    plt.pause(10.0)
    return True

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    query = [args.query]
    auth = twitter_client.get_twitter_auth()
    stream = Stream(auth, MyListener(query))
    stream.filter(track=query, async=True)
    while True:
        if counter:
            display_wordcloud()
