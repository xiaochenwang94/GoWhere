import re
import pandas as pd

data = pd.read_csv('../data/processed_madison.csv')
tweets = data['content']
f = open('../data/stop-word-list.csv', 'r')
line = f.readline()
words = line.split(', ')
patterns = ''
print(words)
for index, word in enumerate(words):
    patterns += word
    if index != len(words)-1:
        patterns+='|'
print(patterns)
result = set()
for tweet in tweets:
    word = tweet.split()
    for w in word:
        if re.match(patterns, w) is not None:
            continue
        w = re.sub('#|!|,','',w)
        result.add(w.lower())
print(result)