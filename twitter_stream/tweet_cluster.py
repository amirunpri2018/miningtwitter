import sys
import json
from argparse import ArgumentParser
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def get_parser():
    parser = ArgumentParser("Clustering of followers")
    parser.add_argument('--filename')
    parser.add_argument('--k', type=int)
    parser.add_argument('--min-df', type=int, default=2)
    parser.add_argument('--max-df', type=float, default=0.8)
    parser.add_argument('--max-features', type=int, default=None)
    parser.add_argument('--no-idf', dest='use_idf', default=True, action='store_false')
    parser.add_argument('--min-ngram', type=int, default=1)
    parser.add_argument('--max-ngram', type=int, default=1)
    return parser

if __name__ == '__main__':
    #parser = get_parser()
    #args = parser.parse_args()
    #if args.min_ngram > args.max_ngram:
    #    print("Error: incorrect value for --min-ngram ({}): it can't be higher than --max-value ({})".format(args.min_ngram, args.max_ngram))
    #    sys.exit(1)

    filename = 'stream_Jimmy_Butler.json'
    k = 5
    min_df = 0.001
    max_df = 0.5
    use_idf = True
    min_ngram = 2
    max_ngram = 2

    with open(filename) as f:
        # load data
        users = []
        for line in f:
            tweet = json.loads(line)
            profile = tweet['user']
            if profile['description']:
                users.append(profile['description'])
        # create vectorizer
        vectorizer = TfidfVectorizer(max_df=max_df,
                                     min_df=min_df,
                                     #max_features=max_features,
                                     stop_words='english',
                                     ngram_range=(min_ngram, max_ngram),
                                     use_idf=use_idf)
        # fit data
        X = vectorizer.fit_transform(users)
        print("Data dimensions: {}".format(X.shape))
        # perform clustering
        km = KMeans(n_clusters=k)
        km.fit(X)
        clusters = defaultdict(list)
        for i, label in enumerate(km.labels_):
            clusters[label].append(users[i])
        # print 10 user description for this cluster
        for label, descriptions in clusters.items():
            print('---------- Cluster {}'.format(label))
            for desc in descriptions[:10]:
                print(desc)
