#-*- coding:utf-8 -*-
import os
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np
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


def score(data, word):
    idx = []
    band_width = 1e-4
    print('word is %s' % word)

    for i in range(data.shape[0]):
        # print(data.iloc[i]['tweets'].split())
        if word in data.iloc[i]['tweets'].split():
            idx.append(i)
    if idx.__len__() < 5:
        return Result(word, -1)
    # print(idx.__len__())
    # a = input("print idx......")
    # print(idx)
    selx = list(data.iloc[idx]['long'] - madison_long)
    sely = list(data.iloc[idx]['lati'] - madison_lati)
    values = np.vstack([selx,sely])
    # a = input("print values......")
    # print(selx)
    # print(sely)
    # print(values)
    # a = input()
    try:
        kernel = stats.gaussian_kde(values, bw_method='scott')
    except:
        return Result(word, -1)
    print(word,kernel((0,0)),idx.__len__())
    # a = input()
    return Result(word,kernel((0,0)))



def kde(data, check, k=5):
    print('Using kernel density estimation......')
    # 选出check当天的所有数据
    select = data[data['time'] == check.date]
    print('date: %s \n dataset shape %s' %(check.date, select.shape[0]) )
    # 总结出当天的word list
    word_list = set()
    # print(select.shape)
    for idx in range(select.shape[0]):
        w = set(select.iloc[idx]['tweets'].split())
        word_list = word_list | w
    # print(word_list)

    # 计算每个单词的概率,排序
    result = []
    print('word list size is %s' % word_list.__len__())
    for word in word_list:
        r = score(select,word)
        if r.score != -1:
            result.append(r)

    # sort result
    result.sort()
    return result[:k]


def annotate(tweets, checkins):
    print('Start annotation......')
    print('Tweets dataset shape %s' % tweets.shape[0])
    print('Checkins dataset shape %s' % checkins.shape[0])
    ret = {}
    for idx in range(checkins.shape[0]):
        words = kde(tweets, checkins.iloc[idx])

    print('annotation ended......')
    return ret

if __name__ == '__main__':
    if not os.path.isfile('../data/processed_data.csv'):
        process_data()
    if not os.path.isfile('../data/processed_madison.csv'):
        process_foursquare()
    tweets = pd.read_csv('../data/processed_data.csv')
    fsq = pd.read_csv('../data/processed_madison.csv')
    annotation = annotate(tweets, fsq)
    print('end......')















