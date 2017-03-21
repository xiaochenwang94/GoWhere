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

def process_data(data):
    print('Processing data......')
    for i in data['time'].index:
        # data['time'][i] = datetime.strptime(data['time'][i], '%Y-%m-%dT%H:%M:%S')
        # tmp = datetime.strptime(data['time'][i], '%Y-%m-%dT%H:%M:%S')
        # print(pd.to_datetime(str(pd.to_datetime(data['time'])[i]).split()[0]))
        # data['time'][i] = pd.to_datetime(str(pd.to_datetime(data['time'])[i]).split()[0])
        data['time'][i] = str(pd.to_datetime(data['time'])[i]).split()[0]
        if i % 100 == 0:
            print(i, data['time'][i])
    data.to_csv('../data/processed_data.csv')
    print('Data after processing is stored in processed_data.csv.')

def process_foursquare(data):
    print('Processing foursquare data......')
    for i in data['date'].index:
        data['date'][i] = datetime.strftime(data['time'][i],'')
    pass


def score(data, word):
    L = 0
    s = 0
    for d in data:
        if word in d['tweets'].split():
            L += 1
            s += stats.gaussian_kde()
    return Result(word, s/L)

def kde(data, check, k=5):
    # 选出check当天的所有数据
    select = data[data['time'] == check.time]
    # 总结出当天的word list
    word_list = ([x for x in select['tweets'].split()])
    print(word_list)
    # 计算每个单词的概率,排序
    result = []
    for word in word_list:
        result.append(score(select, word))
    # sort result
    return result[:k]



if __name__ == '__main__':
    if not os.path.isfile('../data/processed_data.csv'):
        data = pd.read_csv('../data/data_NewYork.csv')
        process_data(data)
    # if not os.path.isfile('./processed_madison.csv'):
    #     foursquare = pd.read_csv('./madison.csv')
    #     process_foursquare(foursquare)
    # d = pd.read_csv('./processed_data.csv')
    # print(type(foursquare))















