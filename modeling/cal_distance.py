import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from haversine import  haversine, Unit
from tqdm import tqdm


def cal_distance(basic_df, object_df):
    item_id = basic_df['item_id'].unique()
    station_name = object_df['station_name'].unique()

    df = pd.DataFrame(basic_df['item_id'].copy())
    df.set_index('item_id', inplace=True)
    for name in station_name:
        df[name] = 0

    for id in tqdm(item_id):
        for name in station_name:
            item = basic_df[basic_df['item_id']==id][['latitude', 'longitude']].values
            station = object_df[object_df['station_name']==name][['latitude', 'longitude']].values
            item_ = (item[0][0], item[0][1])
            station_ = (station[0][0], station[0][1])
            
            df.loc[id, name] = int(haversine(item_, station_, unit='m'))

    return df

if __name__=="__main__":
    
    data_path = '../data/'
    basic_df = pd.read_csv(data_path+'basic_data.csv')
    object_df = pd.read_csv(data_path+'seoul.csv')

    df = cal_distance(basic_df, object_df)
    df.to_csv(data_path+'basic_station_seoul.csv')