mport numpy as np
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import warnings
warnings.filterwarnings(action='ignore')


def match_grid_id():
    engine = create_engine(f'mysql+pymysql://아이디:비밀번호@DBIP:3306/Database명칭', echo=False,poolclass=NullPool)

    # dong_crawling 에서 크롤링된 데이터 정보
    house_info_df = pd.read_csv('./data/house_info.csv')
    # 기존에 서울시를 25x25 격자로 나누어둔 정보
    # 이 정보가 csv 로 존재하기 때문에 dong_crawling 에서도 csv 사용 
    grid_df = pd.read_csv('./data/grid_20230111_200538_withoutInfra.csv')

    house_info_df['grid_id']=-1

    for index, row in tqdm(house_info_df.iterrows(), total=house_info_df.shape[0]):
        idx = grid_df[( grid_df['min_lat'] < row['lat'] ) & ( row['lng'] < grid_df['max_lat'] )  & ( grid_df['min_long'] < row['lng'] ) & ( row['lat'] < grid_df['max_long'] )].index[0]
        house_info_df.loc[index,['grid_id']] = grid_df.iloc[idx]['id']

    house_info_df.to_sql('house_info_with_grid', index=False, con=engine,if_exists='replace',dtype={
        'item_id':Integer,
        'user_no':Integer,
        'sales_type':VARCHAR(2),
        'sales_title':VARCHAR(2),
        'service_type':VARCHAR(4),
        'images':Text,
        'image_thumbnail':Text,
        'images_cnt':Integer,
        '매매금액':Integer,
        '보증금액':Integer,
        '월세금액':Integer,
        '전용면적_m2':Float,
        '공급면적_m2':Float,
        '대지권면적_m2':Float,
        'address':VARCHAR(32),
        'jibunAddress': VARCHAR(32),
        'local1':VARCHAR(12),
        'local2':VARCHAR(12),
        'local3':VARCHAR(12),
        'local4':VARCHAR(12),
        'room_type_code':Integer,
        'room_type':VARCHAR(5),
        'title':VARCHAR(256),
        'status':CHAR(10),
        'description':Text,
        'secret_memo':Text,
        'is_zzim':CHAR(4),
        'random_location':VARCHAR(64),
        'lat':Float,
        'lng':Float,
        'parking':VARCHAR(12),
        'elevator':Integer,
        'room_direction':CHAR(4),
        'movein_date':VARCHAR(64),
        'agent_comment':Text,
        'pnu':CHAR(32),
        'floor':VARCHAR(8),
        'floor_string':VARCHAR(8),
        'floor_all':VARCHAR(8),
        'pets':Text,
        'loan':Text,
        'building_id':Text,
        'options':VARCHAR(52),
        'manage_cost':Integer,
        'manage_cost_inc':VARCHAR(52),
        'is_realestate':Integer,
        'is_room':Integer,
        'is_owner':Integer,
        'is_premium':Integer,
        'is_homepage':Integer,
        'user_has_penalty':Integer,
        'building_type':Integer,
        'room_gubun_code':CHAR(8),
        'view_count':Integer,
        'updated_at':CHAR(24),
        'is_first_movein':Integer,
        'vr_key':Text,
        'vr_type_name':Text,
        'approve_date':VARCHAR(24),
        'bathroom_count':Integer,
        'residence_type':VARCHAR(100),
        'manage_cost_not_inc':CHAR(52),
        'popular':JSON,
        '자동종료대상':Integer,
        '상태확인At':VARCHAR(24),
        '자동종료At':VARCHAR(24),
    })                                                                                                         37,1          64%                                                                                                         1,1           Top