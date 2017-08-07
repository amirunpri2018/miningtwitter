import json
import operator 
import string
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk import bigrams
from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT','rt','via','…'+',']

with open('stream_Jimmy_Butler.json', 'r') as f:
    com = defaultdict(lambda : defaultdict(int))
    count_all = Counter()   
    count_bigram = Counter()
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        tknz = TweetTokenizer()
        tknztweet = tknz.tokenize(tweet['text'])
        terms_only = [term for term in tknztweet if term not in stop and not term.startswith(('@','#'))]
        terms_hash = [term for term in tknztweet if term.startswith('#')]
        terms_mention = [term for term in tknztweet if term.startswith('@')]
        count_all.update(terms_only)
        terms_bigram = bigrams(terms_only)
        count_bigram.update(terms_bigram)
        # Build co-occurrence matrix
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1

    com_max = []
    # For each term, look for the most common co-occurrent terms
    for t1 in com:
        t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
        for t2, t2_count in t1_max_terms:
            com_max.append(((t1, t2), t2_count))
    # Get the most frequent co-occurrences
    terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
    #words = terms_max[:5]
    #print(count_bigram.most_common(5))
    # Print the first 5 most frequent words
    words = count_all.most_common(10)

wordsdict = {}
for w in words:
    wordsdict[w[0]]=w[1]

plt.bar(range(len(wordsdict)), wordsdict.values(), align='center')
plt.xticks(range(len(wordsdict)), wordsdict.keys())

plt.show()


# Pretty print of json-line
#print(json.dumps(tweet, indent=4))
