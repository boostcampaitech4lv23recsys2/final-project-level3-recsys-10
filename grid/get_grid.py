import numpy as np
import pandas as pd
import argparse
from haversine import haversine
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import time
import math
from tqdm import tqdm

def make_grid(map_min_lat: float, map_max_lat: float, map_min_long: float, map_max_long: float) -> pd.DataFrame:
    print("make_grid start!")
    grid_len = 25
    w = haversine((map_min_lat,map_min_long),(map_min_lat,map_max_long)) * 1000 # m로 변환
    h = haversine((map_min_lat,map_min_long),(map_max_lat,map_min_long)) * 1000
    
    w_box = w//grid_len + 1
    h_box = h//grid_len + 1
    
    x_itv = (map_max_long - map_min_long)/w_box
    y_itv = (map_max_lat - map_min_lat)/h_box
    
    grid_df = pd.DataFrame({'id':[],'main_long':[],'main_lat':[],'min_long':[],'max_long':[],'min_lat':[],'max_lat':[]})
    # start = time.time()
    # for i_y,k_y in enumerate(tqdm(np.arange(map_min_lat, map_max_lat,y_itv))):
    #     for i_x,k_x in enumerate(np.arange(map_min_long, map_max_long,x_itv)):
    #         tmp_x = k_x + 0.5 * x_itv
    #         tmp_y = k_y + 0.5 * y_itv
    #         grid_df.loc[i_y * w_box + i_x] = [i_y * w_box + i_x, k_x + 0.5 * x_itv, k_y + 0.5 * y_itv, k_x, k_x + x_itv, k_y, k_y + y_itv]
    # grid_df['id'] = grid_df['id'].apply(lambda x: int(x))
    # end = time.time()
    # print(f"make_grid: {end - start:.5f} sec")
    return grid_df

def make_infra_columns(grid_df: pd.DataFrame, infra_df: pd.DataFrame, infra_name: str, radius: float) -> pd.DataFrame:
    
    long_km = 0.01175
    lat_km = 0.009
    
    print(f"make_{infra_name}_columns start!")
    # grid_df[infra_name + '_dist'] = 1000000
    # grid_df[infra_name + '_cnt'] = 0        
    
    start = time.time()
    for index_g, row_g in tqdm(grid_df.iterrows(), total=grid_df.shape[0]):
        min_dist = 1000000
        cnt = 0
    
        filterd_infra_df = infra_df[(row_g['main_lat']-radius*1.1*lat_km<infra_df['위도']) & (infra_df['위도']<row_g['main_lat']+radius*1.1*lat_km) & (row_g['main_long']-radius*1.1*long_km<infra_df['경도']) & (infra_df['경도']<row_g['main_long']+radius*1.1*long_km)]
        for index_t, row_t in filterd_infra_df.iterrows():
            tmp = haversine((row_g['main_lat'],row_g['main_long']),(row_t['위도'],row_t['경도']))
            if tmp < radius: 
                cnt+=1
                min_dist = min(min_dist, tmp)
        grid_df.loc[index_g,infra_name + '_dist']=min_dist
        grid_df.loc[index_g,infra_name + '_cnt']=cnt
        
    end = time.time()
    grid_df.loc[grid_df[infra_name + '_dist']==1000000,infra_name + '_dist']=-1
    print(f"make_{infra_name}_columns: {end - start:.5f} sec")
    return grid_df

def make_score_columns(grid_df: pd.DataFrame, infra_name: str, radius: float) -> pd.DataFrame: # 축약어로 컬럼명을 넣은 경우 축약어를 넘겨줘야함.
    mms = MinMaxScaler()
    ss = StandardScaler()
    
    col_name = infra_name + '_dist'
    grid_df[col_name+'_score'] = 0
    tmp = grid_df[grid_df[col_name]!=-1][[col_name]].apply(lambda x: abs(x-radius))
    tmp = ss.fit_transform(tmp)
    tmp = mms.fit_transform(tmp)
    # grid_df.loc[grid_df[col_name]!=-1, [col_name + '_score']] = ss.fit_transform(grid_df[grid_df[col_name]!=-1][[col_name]])
    # grid_df.loc[grid_df[col_name]!=-1, [col_name + '_score']] = mms.fit_transform(grid_df[grid_df[col_name]!=-1][[col_name + '_score']])
    grid_df.loc[grid_df[col_name]!=-1,[col_name + '_score']] = tmp
    # grid_df.loc[grid_df[col_name]==-1,col_name + '_score'] = 0
    
    col_name = infra_name + '_cnt'
    grid_df[col_name+'_score'] = 0
    tmp = pd.DataFrame(grid_df.loc[grid_df[col_name]!=0,col_name].apply(lambda x: math.log(1+x)))
    tmp = ss.fit_transform(tmp)
    tmp = mms.fit_transform(tmp)
    grid_df.loc[grid_df[col_name]!=0, [col_name + '_score']] = tmp
    return grid_df

def main(args):
    print("main start!")
    start = time.time()
    ## Data load
    park = pd.read_csv(args.DATA_PATH + 'park_data_v1.1.csv')
    mart = pd.read_csv(args.DATA_PATH + 'mart_data.csv')
    cs = pd.read_csv(args.DATA_PATH + 'cs_data.csv')
    cafe = pd.read_csv(args.DATA_PATH + 'cafe_data_v1.1.csv')
    pharmacy = pd.read_csv(args.DATA_PATH + 'pharmacy_data_v2.0.csv')
    subway = pd.read_csv(args.DATA_PATH + 'subway_data_v1.2.csv')
    theater = pd.read_csv(args.DATA_PATH + 'theater_data_v1.2.csv')
    
    grid_df = make_grid(args.COORD[0], args.COORD[1], args.COORD[2], args.COORD[3])
    
    grid_df = make_infra_columns(grid_df,theater,'theater',2)
    grid_df = make_score_columns(grid_df,'theater',2)

    grid_df = make_infra_columns(grid_df,pharmacy,'phar',0.5)
    grid_df = make_score_columns(grid_df,'phar',0.5)

    grid_df = make_infra_columns(grid_df,subway,'subway',0.5)
    grid_df = make_score_columns(grid_df,'subway',0.5)

    grid_df = make_infra_columns(grid_df,cafe,'cafe',0.3)
    grid_df = make_score_columns(grid_df,'cafe',0.3)

    grid_df = make_infra_columns(grid_df,cs,'cs',0.3)
    grid_df = make_score_columns(grid_df,'cs',0.3)
    
    now = time.localtime()
    now_date = time.strftime('%Y%m%d', now)
    now_hour = time.strftime('%X', now)
    save_time = now_date + '_' + now_hour.replace(':', '')
    
    grid_df.to_csv(args.OUTPUT_PATH + 'grid_' + save_time + '.csv', index=False)
    end = time.time()
    print(f"main: {end - start:.5f} sec")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parser')
    arg = parser.add_argument

    arg('--DATA_PATH', type=str, default='data/', help='Data path 설정')
    arg('--COORD', type=float, nargs=4, help='[min_long, max_long, min_lat, max_lat]로 최소최대 위경도 설정 ')
    arg('--OUTPUT_PATH', type=str, default='output/',help='Output path 설정')

    args = parser.parse_args()
    main(args)
