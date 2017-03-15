#-*- coding:utf-8 -*-
import os
import pandas as pd
from datetime import datetime

def process_data(data):
    print('Processing data......')
    for i in data['time'].index:
        data['time'][i] = datetime.strptime(data['time'][i], '%Y-%m-%dT%H:%M:%S')
        if i % 100 == 0:
            print(i, data['time'][i])
    data.to_csv('../data/processed_data.csv')
    print('Data after processing is stored in processed_data.csv.')







if __name__ == '__main__':
    if not os.path.isfile('../data/processed_data.csv'):
        data = pd.read_csv('../data/data_NewYork.csv')
        process_data(data)