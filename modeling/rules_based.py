import numpy as np
import pandas as pd
import pyproj
import geopy
import matplotlib as mpl
import matplotlib.pyplot as plt
from haversine import haversine
from args import arg_parse

import warnings
warnings.filterwarnings(action='ignore')

import os
from tqdm import tqdm

pd.options.display.max_columns = 100

def recommendation(user_name, loc, inf, item, grid):
    item = item[(item['local2'] == loc) & (item['status']=='open')]
    # item = item[item['local2'] == loc]
    
    # 위도, 경도 나누기 -> 데이터 따로 저장해두면 생략 가능할 듯
    for index, row in tqdm(item.iterrows(),total=item.shape[0]):
        item.loc[index,'위도'] = float(row['random_location'].split(',')[0])
        item.loc[index,'경도'] = float(row['random_location'].split(',')[1])
    
    item = item[['item_id','sales_type','jibunAddress','위도','경도','service_type','local2','보증금액','월세금액','전용면적_m2','공급면적_m2']]

    cols = ['theater_dist', 'theater_cnt', 'theater_dist_score', 'theater_cnt_score', 
            'phar_dist', 'phar_cnt', 'phar_dist_score', 'phar_cnt_score', 
            'subway_dist', 'subway_cnt', 'subway_dist_score', 'subway_cnt_score', 
            'cafe_dist', 'cafe_cnt', 'cafe_dist_score', 'cafe_cnt_score', 
            'cs_dist', 'cs_cnt', 'cs_dist_score', 'cs_cnt_score']
    
    # 범위 내에 포함되면 체크
    for i in tqdm(item.index):
        t =  grid[(grid['min_lat']<item.loc[i,'위도']) & (item.loc[i,'위도']<grid['max_lat']) & (grid['min_long'] < item.loc[i,'경도']) & (item.loc[i,'경도']<grid['max_long'])]
        item.loc[i,cols] = t[cols].squeeze()
    
    # total score
    item['total_score'] = 0
    infra_num = len(list(args.select_infra.split(',')))
    if '영화관' in list(args.select_infra.split(',')):
        item['total_score']+=item['theater_dist_score']
    if '약국' in list(args.select_infra.split(',')):
        item['total_score']+=item['phar_dist_score']
    if '지하철' in list(args.select_infra.split(',')):
        item['total_score']+=item['subway_dist_score']
    if '카페' in list(args.select_infra.split(',')):
        item['total_score']+=item['cafe_dist_score']
    if '편의점' in list(args.select_infra.split(',')):
        item['total_score']+=item['cs_dist_score']
    item['total_score'] = item['total_score']/infra_num*100

    # item['total_score'] = item['theater_dist_score'] + item['phar_dist_score'] + item['subway_dist_score'] + item['cafe_dist_score'] + item['cs_dist_score']

    # sort & top 10
    item = item.sort_values('total_score',ascending=False)
    result = item[:10][['item_id', 'jibunAddress', 'service_type', 'sales_type', '보증금액', '월세금액', '경도', '위도', 'total_score']]

    return result


def main(args):
    data_path = args.data_path
    grid = pd.read_csv(data_path + args.grid_file)
    item = pd.read_csv(data_path + args.infra_file)

    user_name = args.user_name
    loc = args.user_loc
    inf = args.select_infra

    result = recommendation(user_name, loc, inf, item, grid)

    print(result)



if __name__=='__main__':
    args = arg_parse()
    main(args)