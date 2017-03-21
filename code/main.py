#-*- coding:utf-8 -*-
import os
import pandas as pd
from scipy import stats
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

class Result(object):

    def __init__(self, w='', s=0.0):
        self.word = w
        self.score = s

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
    # L = 0
    # s = 0
    # for d in data:
    #     if word in d['tweets'].split():
    #         L += 1
    #         s += stats.gaussian_kde()
    # return Result(word, s/L)
    sel = data[word in data]


def kde(data, check, k=5):
    # 选出check当天的所有数据
    # print(data.head())
    select = data[data['time'] == check.date]
    # 总结出当天的word list
    word_list = set()
    print(select.shape)
    for idx in range(select.shape[0]):
        w = set(select.iloc[idx]['tweets'].split())
        word_list = word_list | w
    print(word_list)
    # 计算每个单词的概率,排序
    result = []
    for word in word_list:
        result.append(score(select, word))
    # sort result
    # return result[:k]

def annotate(tweets, checkins):
    ret = {}
    print(type(checkins))
    for idx in range(checkins.shape[0]):
        words = kde(tweets, checkins.iloc[idx])
        w = input()
        # ret[checkin] = words
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















