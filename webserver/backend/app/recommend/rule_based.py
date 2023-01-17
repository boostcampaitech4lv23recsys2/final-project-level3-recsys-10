import numpy as np
import pandas as pd

from sqlalchemy.orm import Session
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick
# from . import schemas

import warnings
warnings.filterwarnings(action='ignore')

import os
# from tqdm import tqdm

# pd.options.display.max_columns = 100

def inference_gu(user_id, user_gu, db: Session):
    s = f"""
    SELECT H.house_id,
            RANK() over (ORDER BY (SUM(G.infra_dist_score) + SUM(G.infra_cnt_score)) DESC, H.house_id) as ranking
    FROM HOUSE_INFO H,
            GRID_SCORE G
    WHERE H.grid_id = G.grid_id
       	AND local2 = "{user_gu}"
        AND G.INFRA_TYPE IN (SELECT U.infra_type
                            FROM USERS_INFRA U
                            where U.user_id = {user_id}
                                AND U.infra_yn = 'Y')
    GROUP BY H.house_id
    ORDER BY ranking 
    """
    return db.execute(s).all()


def inference_latlng(user_id, min_lat, min_lng, max_lat, max_lng, db: Session):
    s = f"""
    SELECT H.house_id,
            RANK() over (ORDER BY (SUM(G.infra_dist_score) + SUM(G.infra_cnt_score)) DESC, H.house_id) as ranking
    FROM HOUSE_INFO H,
            GRID_SCORE G
    WHERE H.grid_id = G.grid_id
        AND H.lat >= {min_lat}
        AND H.lat <= {max_lat}
        AND H.lng >= {min_lng}
        AND H.lng <= {ßmax_lng}
        AND G.INFRA_TYPE IN (SELECT U.infra_type
                            FROM USERS_INFRA U
                            where U.user_id = {user_id}
                                AND U.infra_yn = 'Y')
    GROUP BY H.house_id
    ORDER BY ranking 
    """
    return db.execute(s).all()

# def recommendation(user_name, loc, inf, item, grid):
#     parser = argparse.ArgumentParser()
#     # parser.add_argument('--data_path', type=str, default='../data/', help='data path')
#     # parser.add_argument('--grid_file', type=str, default='grid_infra_data_v1.1.csv', help='frid file name')
#     # parser.add_argument('--infra_file', type=str, default='raw_data/직방크롤링원룸오피스텔.csv', help='infra score file name')

#     parser.add_argument('--user_name', type=str, default='1', help='name of user')
#     parser.add_argument('--user_loc', type=str, default='강남구', help='location selected')
    
#     parser.add_argument('--select_infra', type=str, default='영화관,약국,지하철,카페,편의점', help='infra selected')

#     args = parser.parse_args()


#     item = item[(item['local2'] == loc) & (item['status']=='open')]
#     # item = item[item['local2'] == loc]
    
#     # 위도, 경도 나누기 -> 데이터 따로 저장해두면 생략 가능할 듯
#     for index, row in tqdm(item.iterrows(),total=item.shape[0]):
#         item.loc[index,'위도'] = float(row['random_location'].split(',')[0])
#         item.loc[index,'경도'] = float(row['random_location'].split(',')[1])
    
#     item = item[['item_id','sales_type','jibunAddress','위도','경도','service_type','local2','보증금액','월세금액','전용면적_m2','공급면적_m2']]

#     cols = ['theater_dist', 'theater_cnt', 'theater_dist_score', 'theater_cnt_score', 
#             'phar_dist', 'phar_cnt', 'phar_dist_score', 'phar_cnt_score', 
#             'subway_dist', 'subway_cnt', 'subway_dist_score', 'subway_cnt_score', 
#             'cafe_dist', 'cafe_cnt', 'cafe_dist_score', 'cafe_cnt_score', 
#             'cs_dist', 'cs_cnt', 'cs_dist_score', 'cs_cnt_score']
    
#     # 범위 내에 포함되면 체크
#     for i in tqdm(item.index):
#         t =  grid[(grid['min_lat']<item.loc[i,'위도']) & (item.loc[i,'위도']<grid['max_lat']) & (grid['min_long'] < item.loc[i,'경도']) & (item.loc[i,'경도']<grid['max_long'])]
#         item.loc[i,cols] = t[cols].squeeze()
    
#     # total score
#     item['total_score'] = 0
#     infra_num = len(list(args.select_infra.split(',')))
#     if '영화관' in list(args.select_infra.split(',')):
#         item['total_score']+=item['theater_dist_score']
#     if '약국' in list(args.select_infra.split(',')):
#         item['total_score']+=item['phar_dist_score']
#     if '지하철' in list(args.select_infra.split(',')):
#         item['total_score']+=item['subway_dist_score']
#     if '카페' in list(args.select_infra.split(',')):
#         item['total_score']+=item['cafe_dist_score']
#     if '편의점' in list(args.select_infra.split(',')):
#         item['total_score']+=item['cs_dist_score']
#     item['total_score'] = item['total_score']/infra_num*100

#     # item['total_score'] = item['theater_dist_score'] + item['phar_dist_score'] + item['subway_dist_score'] + item['cafe_dist_score'] + item['cs_dist_score']

#     # sort & top 10
#     item = item.sort_values('total_score',ascending=False)
#     result = item[:10][['item_id', 'jibunAddress', 'service_type', 'sales_type', '보증금액', '월세금액', '경도', '위도', 'total_score']]

#     return result


# def main(args):
#     # data_path = args.data_path
#     # grid = pd.read_csv(data_path + args.grid_file)
#     # item = pd.read_csv(data_path + args.infra_file)

#     # user_name = args.user_name
#     # loc = args.user_loc
#     # inf = args.select_infra

#     # result = recommendation(user_name, loc, inf, item, grid)

#     return {}



# if __name__=='__main__':
#     args = arg_parse()
#     main(args)