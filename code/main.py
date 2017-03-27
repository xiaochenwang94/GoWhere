#-*- coding:utf-8 -*-
import os
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

madison_long = -73.993278
madison_lati = 40.750456


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
    tmp = data[data['date'] < '2010-03-10']
    tmp = tmp[tmp['date'] > '2010-03-01']
    # print(data['date'])
    tmp.to_csv('../data/processed_madison.csv')
    print('4sq data processed.')


def score(word, locations):
    if len(locations) < 5:
        return Result(word, -1)
    band_width = 1e-4
    selx = []
    sely = []
    for lati, long in locations:
        selx.append(long - madison_long)
        sely.append(lati- madison_lati)
    values = np.vstack([selx,sely])
    try:
        kernel = stats.gaussian_kde(values, bw_method='scott')
    except:
        return Result(word, -1)
    if len(locations) > 1000:
        selx = np.array(selx)
        sely = np.array(sely)
        xmin = selx.min()
        xmax = selx.max()
        ymin = sely.min()
        ymax = sely.max()
        X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        Z = np.reshape(kernel(positions).T, X.shape)
        fig, ax = plt.subplots()
        ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,
                  extent=[xmin, xmax, ymin, ymax])
        ax.plot(selx, sely, 'r.', markersize=2)
        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        print(word, kernel((0,0)))
        plt.show()
    return Result(word,kernel((0,0)))



def kde(data, check, k=5):
    print('Using kernel density estimation......')
    # 选出check当天的所有数据
    select = data[data['time'] == check.date]
    print('date: %s \ndataset shape %s' % (check.date, select.shape[0]))
    # 总结出当天的word list
    word_list = defaultdict(list)
    filter_words = ['to','on','me','u','not','get','i\'m','be','in','the','i'
                    'it','but','got','my','and','of','so','up','was','all',
                    'that','this','you','he','she','like','for']
    for index, row in select.iterrows():
        words = set(row['tweets'].split())
        for w in words:
            w = w.lower()
            if w in filter_words:
                continue
            word_list[w].append((row['lati'], row['long']))
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


def annotate(tweets, checkins):
    print('Start annotation...')
    print('Tweets dataset shape %s' % tweets.shape[0])
    print('Checkins dataset shape %s' % checkins.shape[0])
    ret = {}
    for index, row in checkins.iterrows():
        words = kde(tweets, row)
    # for idx in range(checkins.shape[0]):
    #     words = kde(tweets, checkins.iloc[idx])
    print('annotation ended......')
    return ret

def initialize_data(fsq_file, tweets_file):
    if not os.path.isfile(tweets_file):
        data = pd.read_csv('../data/tweets.csv')
        


if __name__ == '__main__':

    fsq_file = '../data/fsq.csv'
    tweets_file = '../data/tweets_processed.csv'
    initialize_data(fsq_file, tweets_file)

    # if not os.path.isfile('../data/processed_data.csv'):
    #     process_data()
    # if not os.path.isfile('../data/processed_madison.csv'):
    #     process_foursquare()
    #
    # tweets = pd.read_csv('../data/processed_data.csv')
    # fsq = pd.read_csv('../data/processed_madison.csv')
    # annotation = annotate(tweets, fsq)
    # print('end......')















