import numpy as np
import os
import pandas as pd
import re

from collections import defaultdict

class Result(object):

    def __init__(self, w='', s=0.0):
        self.word = w
        self.score = s

    def __lt__(self, other):
        return self.score > other.score

class Annotation(object):

    def __init__(self):
        self.tweets = None
        self.checkins = None
        self.stop_words = None
        self.anntate_words = {}
        self.patterns = ''

    def initialize_data(self, fsq_file, tweets_file, stop_words_file):
        print('Initializing data...')
        if not os.path.isfile(tweets_file):
            print('File %s not exists, read tweets.csv' % tweets_file)
            data = pd.read_csv('../data/tweets.csv',encoding='ISO-8859-1')
            idx = data['Latitude'] <= 42
            idx &= data['Latitude'] >= 38
            idx &= data['Longitude'] <= -72
            idx &= data['Longitude'] >= -76
            data = data[idx]
            data = data.set_index('Tweet Id', inplace=False, drop=True)
            data.to_csv(tweets_file, encoding='utf8')
        if not os.path.isfile(fsq_file):
            data = pd.read_csv('../data/madison.csv')
            print('Processing foursquare data......')
            data['date'] = pd.to_datetime(data['date'], errors='coerce')
            tmp = data[data['date'] < '2016-04-20']
            tmp = tmp[tmp['date'] > '2016-04-14']
            tmp.to_csv(fsq_file)
            print('4sq data processed.')
        self.tweets = pd.read_csv(tweets_file)
        self.checkins = pd.read_csv(fsq_file)
        f = open(stop_words_file, 'r')
        line = f.readline()
        self.stop_words = line.split(', ')
        for index, word in enumerate(self.stop_words):
            self.patterns += word
            if index != len(self.stop_words)-1:
                self.patterns+='|'
        print('Initialize finished')
        print('Tweets num = %d' % self.tweets.shape[0])
        print('Checkins num = %d' % self.checkins.shape[0])
        print('Stop words num = %d' % len(self.stop_words))

    def word_filter(self, words):
        words_filted = set()
        for w in words:
            if re.match(self.patterns, w) is not None:
                continue
            w = re.sub('#|!|,','',w)
            if len(w) == 0:
                continue
            words_filted.add(w.lower())
        return words_filted

    def anntation(self):
        print('Start annotation...')
        for index, row in self.checkins.iterrows():
            words = self.kde(row)
            self.anntate_words[index] = words
        print('Anntation ended...')
        return self.anntate_words

    def kde(self, checkin):
        print('Using kernel density estimation...')
        select = self.tweets[self.tweets['Date'] == checkin.date]
        word_list = defaultdict(list)
        for index, row in select.iterrows():
            words = set(row['Tweet content'].split())
            for w in self.word_filter(words):
                word_list[w].append((row['Latitude'], row['Longitude']))
        result = []
        for key, values in word_list.items():
            r = self.score(key, values, checkin)
            result.append(r)
        result.sort()
        return result

    def score(self, word, values, checkin):
        s = 0
        bw = 1e-4
        for value in values:
            s += self.kernel(value[0] - checkin['Latitude'],
                             value[1] - checkin['Longitude'], h=bw)
        s /= len(values)
        return Result(word, s)

    def kernel(self, x, y, h):
        x = np.array([x, y])
        e = np.exp(-1/(2*h)*x.dot(x.T))
        return 1/(2*np.pi*h)*e

if __name__ == '__main__':

    fsq_file = '../data/processed_madison.csv'
    tweets_file = '../data/tweets_processed.csv'
    stop_words_file = '../data/stop-word-list.csv'
    ann = Annotation()
    ann.initialize_data(fsq_file, tweets_file, stop_words_file)
    annotation_doc = ann.anntation()
