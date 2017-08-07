import json
import operator 
import string
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk import bigrams
from collections import Counter
from collections import defaultdict


fname = 'stream_Jimmy_Butler.json'
# Tweets are stored in "fname"
with open(fname, 'r') as f:
    geo_data = {
        "type": "FeatureCollection",
        "features": []  
    }
    for line in f:
        tweet = json.loads(line)
        if tweet['coordinates']:
            print(tweet['coordinates'])
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                    "text": tweet['text'],
                    "created_at": tweet['created_at']
                }
            }
            geo_data['features'].append(geo_json_feature)
 
# Save geo data
with open('geo_data.json', 'w') as fout:
    fout.write(json.dumps(geo_data, indent=4))
