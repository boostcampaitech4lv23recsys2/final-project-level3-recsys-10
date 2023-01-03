import pandas as pd
import numpy as np
import sqlalchemy
import os

from core.config import DATABASE_URL
from utils import setSeeds

def get_db_engine():
    '''Returns a connection and a metadata object'''
    engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)
    #meta = sqlalchemy.MetaData(bind=engine, reflect=True)
    return engine  # , meta


def data_split(raw_interactions, n_all=3, n_seq=1):
    setSeeds()
    print('data split...')
    trains, tests = [], []
    for usr_id, tp in raw_interactions.groupby('user_id', as_index=False):  
        _n_all = min(tp.shape[0]//2, n_all)
        _n_seq = min(_n_all, n_seq)  
        _n_static = _n_all - _n_seq

        _idxs = np.random.permutation(tp.shape[0]-_n_seq)[:_n_static]  # 랜덤으로 추출 (데이터 총 개수 - seq로 뽑아낼 개수)[:seq로 뺼 것 뺴고]
        _mask = tp.index.isin(tp.index[_idxs])
        for i in range(_n_seq):
            _mask[-i-1] = True

        trains.append(tp[~_mask])
        tests.append(tp[_mask])
        
    train_df = pd.concat(trains)
    test_df = pd.concat(tests)
    
    return train_df, test_df


def load_data():
    engine = get_db_engine()
    interactions_df = pd.read_sql("select * from public.interactions", engine)
    recipes_df = pd.read_sql("select * from public.recipes", engine)

    return interactions_df, recipes_df


def save_data_for_recbole(inter_df:pd.DataFrame):
    inter_df.columns = ['user_id:token', 'recipe_id:token', 'date:token', 'rating:float']
    inter_df['rating:float'] = 1
    inter_df = inter_df.sort_values(by='user_id:token')
    
    directory = '/opt/ml/final-project-level3-recsys-13/modeling/RecBole/dataset/foodcom'
    if not os.path.isdir(directory):
        os.makedirs(directory)
        
    inter_df.to_csv(os.path.join(directory, 'foodcom.inter'), index=False)
    
    return