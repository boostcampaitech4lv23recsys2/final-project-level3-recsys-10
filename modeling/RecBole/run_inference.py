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

from recbole.quick_start import (
    load_data_and_model,
    inference_load_data_and_model,
)
from recbole.utils import (
    get_model,
)

if __name__ == '__main__':
    # start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', '-m', type=str, default='saved/model.pth', help='name of models')
    
    args, _ = parser.parse_known_args()
    
    # load model, dataset
    # config, model, dataset, _, _, test_data = load_data_and_model(args.model_path, pretrain=True)
    config, model, dataset, test_data = inference_load_data_and_model(args.model_path, pretrain=True)
    
    # setting device
    device = config.final_config_dict['device']
    
    # user, item id -> token array
    user_id2token = dataset.field2id_token['user_id']
    item_id2token = dataset.field2id_token['house_id']

    # user-item sparse matrix
    matrix = dataset.inter_matrix(form='csr')

    pred_list, user_list, score_list = None, None, None
    
    start = time.time()
    model.eval()
    c=0
    for data in test_data:
        if str(get_model(config['model'])).split('.')[2] == 'general_recommender':
            interaction = data[0].to(device)
            score = model.full_sort_predict(interaction)

            rating_pred = score.cpu().data.numpy().copy()                       # item 개수만큼
            batch_user_index = interaction['user_id'].cpu().numpy()             # user : interaction 있는 user 전체

            matrix_ = list(matrix[batch_user_index].toarray() > 0)[0]           # 현재 interaction 있는 거
            rating_pred[matrix_] = 0                                            #                           제외
            # print('=====================================')
            # print(matrix_)
            # print(len(matrix_))
            # print(rating_pred)
            # print(len(rating_pred))
            # print(batch_user_index)
            # print(len(batch_user_index))
            # print('=====================================')

            # top 10
            ind = np.argpartition(rating_pred, -10)[-10:]                       # 그 중 score 가장 높은거 10개
            arr_ind = rating_pred[ind]

            # sort
            arr_ind_argsort = np.argsort(arr_ind)[::-1]
            batch_pred_list = ind[arr_ind_argsort]

        elif str(get_model(config['model'])).split('.')[2] == 'context_aware_recommender':
            interaction = data[0].to(device)
            score = model.predict(interaction)
            # score = model.full_sort_predict(interaction)

            rating_pred = score.cpu().data.numpy().copy()       # 총 개수 : interaction 수
            batch_user_index = interaction['user_id'].cpu().numpy()

            matrix_ = list(matrix[batch_user_index].toarray() > 0)[0]
            # rating_pred[matrix_] = 0
            # print('=====================================')
            # print(c+1)
            # # print(matrix_)
            # print('len(matrix_) : ', len(matrix_))
            # print(rating_pred)
            # print('len(rating_pred) : ', len(rating_pred))
            # print(batch_user_index)
            # print('len(batch_user_index) : ', len(batch_user_index))
            # print('=====================================')

            # top 10                                                                ###
            ind = np.argpartition(rating_pred, -len(rating_pred))
            # ind = np.argpartition(rating_pred, -10)[-10:]
            arr_ind = rating_pred[ind]

            # sort
            arr_ind_argsort = np.argsort(arr_ind)[::-1]
            batch_pred_list = ind[arr_ind_argsort]

        # save predictions
        if pred_list is None:
            pred_list = batch_pred_list
            user_list = batch_user_index
            score_list = arr_ind
        else:
            pred_list = np.append(pred_list, batch_pred_list, axis=0)
            user_list = np.append(user_list, batch_user_index, axis=0)
            score_list = np.append(score_list, arr_ind, axis=0)
        c+=1
    # print('===========')
    # print('batch_pred_list')
    # print(batch_pred_list)
    # print('===========')

    result = []
    cnt=0
    if str(get_model(config['model'])).split('.')[2] == 'general_recommender':
        # print('==========')
        # print(type(pred_list))
        # print(pred_list)
        # print(len(pred_list))
        # print('==========')
        for user in user_list:
            pred = pred_list[cnt:cnt+10]
            score = score_list[cnt:cnt+10]
            # print('=============')
            # print(user, pred, score)
            # print('=============')
            for item, score_ in zip(pred, score):
                result.append((int(user_id2token[user]), int(item_id2token[item]), score_))
            cnt+=10
    elif str(get_model(config['model'])).split('.')[2] == 'context_aware_recommender':
        # print('==========')
        # print(type(pred_list))
        # # print(pred_list)
        # print(len(pred_list))
        # # print('user')
        # print(len(user_list))
        # print(list(set(user_list)))
        user_unique = list(set(user_list))
        # print(np.where(user_list==list(set(user_list))[3]))
        
        # print('==========')
        for user in user_unique:       # 72
            # print('--------------')
            _index = np.where(user_list==user)
            scr = score_list[_index]
            prd = pred_list[_index]
            scr_sort = np.sort(scr, axis=0)
            scr_argsort = np.argsort(scr_sort)

            pred = prd[scr_argsort][-10:]
            score = scr_sort[-10:]
            for item, score_ in zip(pred, score):
                if item==0:
                    item+=1
                # print(user, item, score_)
                # print((user_id2token[user], item_id2token[item], score_))
                result.append((int(user_id2token[user]), int(item_id2token[item]), score_))
    
    # save submission
    print('inference...')
    dataframe = pd.DataFrame(result, columns=["user", "house", "score"])
    dataframe.sort_values(by=['user','score'], inplace=True)
    dataframe.to_csv(
        f"saved/{config['model']}_submission.csv", index=False
    )
    print('inference done!')
    end = time.time()
    print(f'{round(end - start,10)} sec')