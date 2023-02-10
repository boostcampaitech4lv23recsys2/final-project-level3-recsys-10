import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, LabelEncoder, normalize
from sqlalchemy.orm import Session
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick
from recommend.rule_based import inference_gu #, inference_latlng

import warnings
warnings.filterwarnings(action='ignore')

import os
import sys
import argparse
import shutil

import time

sys.path.append(os.path.realpath(__file__).split('webserver')[0]+'modeling/RecBole/')
from recbole.quick_start import run_recbole
from run_inference import inference


def train_ml_gu(user_id, user_gu, all_user, all_house, zzim_list, click, db: Session):
    start = time.time() # , H.address, H.local2
    s = f"""
            SELECT H.house_id, H.grid_id, H.sales_type, H.service_type, H.house_area, H.price_deposit,
                H.price_monthly_rent, H.manage_cost
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '01' AND infra_yn = 'Y') > 0 THEN G1.infra_dist_score ELSE 0 END as score_1
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '02' AND infra_yn = 'Y') > 0 THEN G2.infra_dist_score ELSE 0 END as score_2
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '03' AND infra_yn = 'Y') > 0 THEN G3.infra_dist_score ELSE 0 END as score_3
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '05' AND infra_yn = 'Y') > 0 THEN G5.infra_dist_score ELSE 0 END as score_5
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '06' AND infra_yn = 'Y') > 0 THEN G6.infra_dist_score ELSE 0 END as score_6
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '07' AND infra_yn = 'Y') > 0 THEN G7.infra_dist_score ELSE 0 END as score_7
                    , CASE WHEN (SELECT COUNT(*) FROM USERS_INFRA WHERE user_id={user_id} AND infra_type = '08' AND infra_yn = 'Y') > 0 THEN G8.infra_dist_score ELSE 0 END as score_8
            FROM HOUSE_INFO2 H
            LEFT JOIN GRID_SCORE G1
                    ON (H.grid_id = G1.grid_id
                        AND G1.infra_type = '01')
            LEFT JOIN GRID_SCORE G2
                    ON (H.grid_id = G2.grid_id
                        AND G2.infra_type = '02')
            LEFT JOIN GRID_SCORE G3
                    ON (H.grid_id = G3.grid_id
                        AND G3.infra_type = '03')
            LEFT JOIN GRID_SCORE G5
                    ON (H.grid_id = G5.grid_id
                        AND G5.infra_type = '05')
            LEFT JOIN GRID_SCORE G6
                    ON (H.grid_id = G6.grid_id
                        AND G6.infra_type = '06')
            LEFT JOIN GRID_SCORE G7
                    ON (H.grid_id = G7.grid_id
                        AND G7.infra_type = '07')
            LEFT JOIN GRID_SCORE G8
                    ON (H.grid_id = G8.grid_id
                        AND G8.infra_type = '08')
            WHERE 1=1
                AND(H.local2 = "{user_gu}"
                        AND H.sold_yn = 'N')
        """

    
    # house
    h_info = pd.DataFrame(db.execute(s).all()
                            , columns=['house_id', 'grid_id', 'sales_type', 'service_type'
                                        , 'house_area', 'price_deposit', 'price_monthly_rent', 'manage_cost'
                                        , 'score_1', 'score_2', 'score_3', 'score_5', 'score_6', 'score_7', 'score_8'])
   
    h_info.loc[h_info[h_info['sales_type']=='월세'].index, 'sales_type'] = 0
    h_info.loc[h_info[h_info['sales_type']=='전세'].index, 'sales_type'] = 1
    h_info.loc[h_info[h_info['service_type']=='오피스텔'].index, 'service_type'] = 0
    h_info.loc[h_info[h_info['service_type']=='원룸'].index, 'service_type'] = 1

    h_info.columns = ['house_id:token', 'grid_id:token', 'sales_type:token', 'service_type:token'
                    , 'house_area:float', 'price_deposit:float', 'price_monthly_rent:float', 'manage_cost:float'
                    , 'score_1:float', 'score_2:float', 'score_3:float', 'score_5:float', 'score_6:float', 'score_7:float', 'score_8:float']
    
    # zzim
    zzim_info = pd.DataFrame(zzim_list, columns=['idx','user_id','house_id','register_date','update_date','zzim_yn'])
    zzim_info['interest'] = 0
    zzim_info.loc[zzim_info[zzim_info['zzim_yn']=='Y'].index, 'interest'] = 5
    zzim_info.loc[zzim_info[zzim_info['zzim_yn']=='N'].index, 'interest'] = 1
    zzim_info = zzim_info[['user_id', 'house_id','interest']]
    zzim_info.columns = ['user_id:token', 'house_id:token', 'interest:float']
    
    # click
    click_info = pd.DataFrame(click, columns=['idx','ip_address','user_id', 'item_id', 'log_type', 'log_date'])
    click_info['interest'] = 3
    click_info = click_info[['user_id', 'item_id', 'interest']]
    click_info.columns = ['user_id:token', 'house_id:token', 'interest:float']
    interaction = pd.concat([zzim_info, click_info])
    
    # user
    user_info = pd.DataFrame(all_user, columns=['user_id', 'name', 'pw', 'user_gu', 'user_age', 'user_sex', 'register_date', 'update_date', 'user_type'])
    user_info = user_info[['user_id', 'name', 'user_gu', 'user_age', 'user_sex', 'user_type']]
    user_info.columns = ['user_id:token','name:token','user_gu:token','user_age:token','user_sex:token','user_type:token']
    
    # save data
    file_path = os.path.realpath(__file__).split('webserver')[0]+'modeling/RecBole/recbole/properties/dataset/'
    shutil.copy(file_path+'rec.yaml',file_path+f'{user_id}.yaml')
    
    path = os.path.realpath(__file__).split('webserver')[0]+'modeling/RecBole/dataset/' + str(user_id) + '/'
    if not os.path.exists(path):
        os.mkdir(path)
    h_info.to_csv(path + str(user_id) + '.item', index=False, sep='\t')
    interaction.to_csv(path + str(user_id) + '.inter', index=False, sep='\t')
    user_info.to_csv(path + str(user_id) + '.user', index=False, sep='\t')

    
    # argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", type=str, default="LightGCN", help="name of models") # MultiVAE, MultiDAE, LightGCN, DCN, FFM
    parser.add_argument(
        "--dataset", "-d", type=str, default=f"{user_id}", help="name of datasets"      # ml-100k sample_rec
    )
    parser.add_argument("--config_files", type=str, default=None, help="config files")
    parser.add_argument("--pretrain", type=str, default=False, help="item coeffs exist")
    args, _ = parser.parse_known_args()
    
    config_file_list = (
        args.config_files.strip().split(" ") if args.config_files else None
    )
    result = run_recbole(user_id=user_id, model=args.model, dataset=args.dataset, config_file_list=config_file_list, pretrain=args.pretrain)

    end = time.time()
    return result


def compare(user_id, zzim_id, infer_id, db: Session):
    path = os.path.realpath(__file__).split('webserver')[0]+'modeling/RecBole/dataset/' + str(user_id) + '/'
    item = pd.read_csv(path + str(user_id) + '.item', sep='\t')

    zzim_item = item[item['house_id:token'].isin(zzim_id)]
    infer_item = item[item['house_id:token'].isin(infer_id)]
    sim = cosine_similarity(zzim_item, infer_item)
    # print(sim)
    print(np.min(sim), np.max(sim))
    return np.mean(sim)


def inference_ml(user_id, zzim_list, click, db: Session):
    result1, result2, result3 = inference(user_id)

    return result1, result2, result3

