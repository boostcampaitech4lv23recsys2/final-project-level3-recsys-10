import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, LabelEncoder, normalize
from sqlalchemy.orm import Session
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick
# from . import schemas

import warnings
warnings.filterwarnings(action='ignore')

import os
# from tqdm import tqdm

# pd.options.display.max_columns = 100

le = LabelEncoder()

def inference_gu_CB(house_id, user_id, user_gu, db: Session):
    s = f"""
            SELECT H.house_id, H.grid_id, H.sales_type, H.service_type, H.house_area, H.price_deposit,
                H.price_monthly_rent, H.manage_cost, H.address, H.local2,
                H.floor_total, H.bathroom_cnt
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '01') > 0 THEN G1.infra_type ELSE 0 END as score_1
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '02') > 0 THEN G2.infra_type ELSE 0 END as score_2
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '03') > 0 THEN G3.infra_type ELSE 0 END as score_3
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '04') > 0 THEN G4.infra_type ELSE 0 END as score_4
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '05') > 0 THEN G5.infra_type ELSE 0 END as score_5
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '06') > 0 THEN G6.infra_type ELSE 0 END as score_6
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '07') > 0 THEN G7.infra_type ELSE 0 END as score_7
            FROM hobbang.HOUSE_INFO2 H
            LEFT JOIN hobbang.GRID_SCORE G1
                    ON (H.grid_id = G1.grid_id
                        AND G1.infra_type = '01')
            LEFT JOIN hobbang.GRID_SCORE G2
                    ON (H.grid_id = G2.grid_id
                        AND G2.infra_type = '02')
            LEFT JOIN hobbang.GRID_SCORE G3
                    ON (H.grid_id = G3.grid_id
                        AND G3.infra_type = '03')
            LEFT JOIN hobbang.GRID_SCORE G4
                    ON (H.grid_id = G4.grid_id
                        AND G4.infra_type = '04')
            LEFT JOIN hobbang.GRID_SCORE G5
                    ON (H.grid_id = G5.grid_id
                        AND G5.infra_type = '05')
            LEFT JOIN hobbang.GRID_SCORE G6
                    ON (H.grid_id = G6.grid_id
                        AND G6.infra_type = '06')
            LEFT JOIN hobbang.GRID_SCORE G7
                    ON (H.grid_id = G7.grid_id
                        AND G7.infra_type = '07')
            WHERE 1=1
                AND((H.local2 = "{user_gu}"
                        AND H.sold_yn = 'N')
                    OR H.house_id = {house_id})
    """

    h_info = pd.read_sql(s, db)

    h_info.set_index('house_id')

    h_info['local3'] = h_info['address'].apply(lambda x: x.split()[1]) # 동 추가
    h_info.drop(['address','grid_id'],axis=1,inplace=True) # 지번주소, 격자 id drop
    
    h_info['sales_type'] = le.fit_transform(h_info['sales_type'])
    h_info['service_type'] = le.fit_transform(h_info['service_type'])
    h_info['local2'] = le.fit_transform(h_info['local2'])
    h_info['local3'] = le.fit_transform(h_info['local3'])

    h_info = pd.DataFrame(normalize(h_info,axis=0))

    return np.argsort(cosine_similarity(h_info.loc[[house_id]],h_info)[0])[::-1][1:6]


def inference_latlng_CB(house_id, user_id, min_lat, max_lat, min_lng, max_lng, db: Session):
    s = f"""
            SELECT H.house_id, H.grid_id, H.sales_type, H.service_type, H.house_area, H.price_deposit,
                H.price_monthly_rent, H.manage_cost, H.address, H.local2,
                H.floor_total, H.bathroom_cnt
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '01') > 0 THEN G1.infra_type ELSE 0 END as score_1
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '02') > 0 THEN G2.infra_type ELSE 0 END as score_2
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '03') > 0 THEN G3.infra_type ELSE 0 END as score_3
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '04') > 0 THEN G4.infra_type ELSE 0 END as score_4
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '05') > 0 THEN G5.infra_type ELSE 0 END as score_5
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '06') > 0 THEN G6.infra_type ELSE 0 END as score_6
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '07') > 0 THEN G7.infra_type ELSE 0 END as score_7
            FROM hobbang.HOUSE_INFO2 H
            LEFT JOIN hobbang.GRID_SCORE G1
                    ON (H.grid_id = G1.grid_id
                        AND G1.infra_type = '01')
            LEFT JOIN hobbang.GRID_SCORE G2
                    ON (H.grid_id = G2.grid_id
                        AND G2.infra_type = '02')
            LEFT JOIN hobbang.GRID_SCORE G3
                    ON (H.grid_id = G3.grid_id
                        AND G3.infra_type = '03')
            LEFT JOIN hobbang.GRID_SCORE G4
                    ON (H.grid_id = G4.grid_id
                        AND G4.infra_type = '04')
            LEFT JOIN hobbang.GRID_SCORE G5
                    ON (H.grid_id = G5.grid_id
                        AND G5.infra_type = '05')
            LEFT JOIN hobbang.GRID_SCORE G6
                    ON (H.grid_id = G6.grid_id
                        AND G6.infra_type = '06')
            LEFT JOIN hobbang.GRID_SCORE G7
                    ON (H.grid_id = G7.grid_id
                        AND G7.infra_type = '07')
            WHERE 1=1
                AND((ST_CONTAINS(ST_POLYFROMTEXT('POLYGON(({min_lng} {min_lat}
                                                        , {min_lng} {max_lat}
                                                        , {max_lng} {max_lat}
                                                        , {max_lng} {min_lat}
                                                        , {min_lng} {min_lat}))')
                                                , H.latlng)
                        AND H.sold_yn = 'N')
                    OR H.house_id = {house_id})
    """

    h_info = pd.read_sql(s, db)

    h_info.set_index('house_id')

    h_info['local3'] = h_info['address'].apply(lambda x: x.split()[1]) # 동 추가
    h_info.drop(['address','grid_id'],axis=1,inplace=True) # 지번주소, 격자 id drop
    
    h_info['sales_type'] = le.fit_transform(h_info['sales_type'])
    h_info['service_type'] = le.fit_transform(h_info['service_type'])
    h_info['local2'] = le.fit_transform(h_info['local2'])
    h_info['local3'] = le.fit_transform(h_info['local3'])

    h_info = pd.DataFrame(normalize(h_info,axis=0))

    return np.argsort(cosine_similarity(h_info.loc[[house_id]],h_info)[0])[::-1][1:6]    