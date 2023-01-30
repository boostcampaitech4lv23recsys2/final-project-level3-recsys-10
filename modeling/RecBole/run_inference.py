# @Time   : 2020/7/20
# @Author : Shanlei Mu
# @Email  : slmu@ruc.edu.cn

# UPDATE
# @Time   : 2022/7/8, 2020/10/3, 2020/10/1
# @Author : Zhen Tian, Yupeng Hou, Zihan Lin
# @Email  : chenyuwuxinn@gmail.com, houyupeng@ruc.edu.cn, zhlin@ruc.edu.cn

import argparse
import torch
import numpy as np
import pandas as pd
from ast import arg

import time

from recbole.quick_start import load_data_and_model
from recbole.utils import (
    get_model,
)

if __name__ == '__main__':
    # start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', '-m', type=str, default='saved/model.pth', help='name of models')
    # python run_inference.py --model_path=/opt/ml/input/RecBole/saved/SASRecF-Apr-07-2022_03-17-16.pth 로 실행
    
    args, _ = parser.parse_known_args()
    
    # load model, dataset
    config, model, dataset, _, _, test_data = load_data_and_model(args.model_path, pretrain=True)
    
    # setting device
    device = config.final_config_dict['device']
    
    # user, item id -> token array
    user_id2token = dataset.field2id_token['user_id']
    item_id2token = dataset.field2id_token['house_id']
    
    # user-item sparse matrix
    matrix = dataset.inter_matrix(form='csr')

    pred_list, user_list = None, None
    

    start = time.time()
    model.eval()
    for data in test_data:
        if str(get_model(config['model'])).split('.')[2] == 'general_recommender':
            interaction = data[0].to(device)
            score = model.full_sort_predict(interaction)

            rating_pred = score.cpu().data.numpy().copy()       # 82441
            batch_user_index = interaction['user_id'].cpu().numpy()

            matrix_ = list(matrix[batch_user_index].toarray() > 0)[0]
            rating_pred[matrix_] = 0

            # top 10
            ind = np.argpartition(rating_pred, -10)[-10:]
            arr_ind = rating_pred[ind]

            # sort
            arr_ind_argsort = np.argsort(arr_ind)[::-1]
            batch_pred_list = ind[arr_ind_argsort]

        else:
            print(str(get_model(config['model'])).split('.')[2])

            interaction = data[0].to(device)
            score = model.predict(interaction)
            print('============================')
            print(score)
            print(len(score))
            
            print('============================')

            rating_pred = score.cpu().data.numpy().copy()       # 82441
            batch_user_index = interaction['user_id'].cpu().numpy()

            rating_pred[matrix[batch_user_index].toarray() > 0] = 0
            
            # top 10
            ind = np.argpartition(rating_pred, -10)[:, -10:]
        
            arr_ind = rating_pred[np.arange(len(rating_pred))[:, None], ind]
            # sort
            arr_ind_argsort = np.argsort(arr_ind)[np.arange(len(rating_pred)), ::-1]
            batch_pred_list = ind[
                np.arange(len(rating_pred))[:, None], arr_ind_argsort
            ]

        # save predictions
        if pred_list is None:
            pred_list = batch_pred_list
            user_list = batch_user_index
        else:
            pred_list = np.append(pred_list, batch_pred_list, axis=0)
            user_list = np.append(user_list, batch_user_index, axis=0)

    result = []
    if str(get_model(config['model'])).split('.')[2] == 'general_recommender':
        cnt=0
        for user in user_list:
            pred = pred_list[cnt:cnt+10]
            for item in pred:
                result.append((int(user_id2token[user]), int(item_id2token[item])))
            cnt+=10
    else:
        for user, pred in zip(user_list, pred_list):
            for item in pred:
                result.append((int(user_id2token[user]), int(item_id2token[item])))
            
    # save submission
    print('inference...')
    dataframe = pd.DataFrame(result, columns=["user", "item"])
    dataframe.sort_values(by='user', inplace=True)
    dataframe.to_csv(
        f"saved/{config['model']}_submission.csv", index=False
    )
    print('inference done!')
    end = time.time()
    print(f'{round(end - start,10)} sec')