#-*- coding:utf-8 -*-
import os
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

# Yankee Stadium 40.829602, -73.926099
# madioson 40.750456 -73.993278
# STAPLES Center 34.043124, -118.267254
madison_long = -73.84640277
madison_lati = 40.75549922


class Result(object):

    def __init__(self, w='', s=0.0):
        self.word = w
        self.score = s

    def __lt__(self, other):
        return self.score > other.score

class CheckIn(object):

    def __init__(self, long=0.0, lati=0.0, t=datetime.now()):
        self.longtitude = long
        self.latitude = lati
        self.ground_truth = []
        self.time = t

def process_data():
    data = pd.read_csv('../data/data_NewYork.csv')
    print('Processing data......')
    for i in data['time'].index:
        data['time'][i] = str(pd.to_datetime(data['time'])[i]).split()[0]
        if i % 100 == 0:
            print(i, data['time'][i])
    data.to_csv('../data/processed_data.csv')
    print('Data after processing is stored in processed_data.csv.')

def process_foursquare():
    data = pd.read_csv('../data/madison.csv')
    print('Processing foursquare data......')
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    tmp = data[data['date'] < '2016-04-20']
    tmp = tmp[tmp['date'] > '2016-04-14']
    # print(data['date'])
    tmp.to_csv('../data/processed_madison.csv')
    print('4sq data processed.')


# def score(word, locations):
#     if len(locations) < 5:
#         return Result(word, -1)
#     band_width = 1e-4
#     selx = []
#     sely = []
#     for lati, long in locations:
#         selx.append(long - madison_long)
#         sely.append(lati- madison_lati)
#     values = np.vstack([selx,sely])
#     try:
#         kernel = stats.gaussian_kde(values, bw_method='scott')
#     except:
#         return Result(word, -1)
#     if len(locations) > 1000:
#         selx = np.array(selx)
#         sely = np.array(sely)
#         xmin = selx.min()
#         xmax = selx.max()
#         ymin = sely.min()
#         ymax = sely.max()
#         X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
#         positions = np.vstack([X.ravel(), Y.ravel()])
#         Z = np.reshape(kernel(positions).T, X.shape)
#         fig, ax = plt.subplots()
#         ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,
#                   extent=[xmin, xmax, ymin, ymax])
#         ax.plot(selx, sely, 'r.', markersize=2)
#         ax.set_xlim([xmin, xmax])
#         ax.set_ylim([ymin, ymax])
#         # print(word, kernel((0,0)))
#         plt.show()
#     return Result(word,kernel((0,0)))

def kernel(x, y, h):
    x = np.array([x, y])
    e = np.exp(-1/(2*h)*x.dot(x.T))
    return 1/(2*np.pi*h)*e

def score(word, values):
    s = 0
    bw = 1e-4
    for value in values:
        s += kernel(value[0] - madison_lati, value[1] - madison_long, h=bw)
    s /= len(values)
    return Result(word, s)

def kde(data, check, stop_words, k=5):
    print('Using kernel density estimation......')
    # 选出check当天的所有数据
    # select = data[data['Date'] == check.date]
    select = data[data['Date'] == '2016-04-16']
    print('date: %s \ndataset shape %s' % (check.date, select.shape[0]))
    # 总结出当天的word list
    word_list = defaultdict(list)
    filter_words = ['to','on','me','u','not','get','i\'m','be','in','the','i'
                    'it','but','got','my','and','of','so','up','was','all',
                    'that','this','you','he','she','like','for']
    for index, row in select.iterrows():
        words = set(row['Tweet content'].split())
        for w in words:
            w = w.lower()
            if w[0] == '#':
                w = w[1:-1]
            if w in stop_words:
                continue
            word_list[w].append((row['Latitude'], row['Longitude']))
    # 计算每个单词的概率,排序
    result = []
    print('word list size is %s' % word_list.__len__())
    for key, value in word_list.items():
        r = score(key, value)
        if r.score != -1:
            result.append(r)
            # print(key, ':', r.score)

    # sort result
    result.sort()
    print("Result.......")
    for r in result[:100]:
        print(r.word, r.score)
    return result[:k]


def annotate(tweets, checkins, stop_words):
    print('Start annotation...')
    print('Tweets dataset shape %s' % tweets.shape[0])
    print('Checkins dataset shape %s' % checkins.shape[0])
    ret = {}
    for index, row in checkins.iterrows():
        words = kde(tweets, row, stop_words)
        a = input('next word\n')
    print('annotation ended......')
    return ret

def initialize_data(fsq_file, tweets_file):
    if not os.path.isfile(tweets_file):
        data = pd.read_csv('../data/tweets.csv',encoding='ISO-8859-1')
        # 34.049770, -118.238735
        idx = data['Latitude'] <= 42
        idx &= data['Latitude'] >= 38
        idx &= data['Longitude'] <= -72
        idx &= data['Longitude'] >= -76
        data = data[idx]
        # data = data.loc[:,['Tweet Id', 'Latitude', 'Longitude',
        #                    'Tweet content','Date']]
        data = data.set_index('Tweet Id', inplace=False, drop=True)
        data.to_csv(tweets_file, encoding='utf8')
    if not os.path.isfile(fsq_file):
        process_foursquare()


if __name__ == '__main__':

    fsq_file = '../data/processed_madison.csv'
    tweets_file = '../data/tweets_processed.csv'
    initialize_data(fsq_file, tweets_file)
    tweets = pd.read_csv('../data/tweets_processed.csv')
    fsq = pd.read_csv('../data/processed_madison.csv')
    f = open('../data/stop-word-list.csv', 'r')
    line = f.readline()
    stop_words = line.split(',')
    annotation = annotate(tweets, fsq, stop_words)
    print('end......')















