import random
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db

from crud import hobbang_crud_test, schemas
from recommend.rule_based import inference_gu #, inference_latlng
from recommend.ML import train_ml_gu, inference_ml, compare
from sklearn.metrics.pairwise import cosine_similarity

# from modeling.RecBole import run_recbole

# from modeling.RecBole.recbole.properties
import sys
import os
import time

router = APIRouter(
    prefix="/recommend",
)

# @router.post("/train")
def train_gu(map: schemas.Items, db: Session = Depends(get_db)):
    # 1. data 확인
    all_user = hobbang_crud_test.get_users(db)
    all_house = hobbang_crud_test.get_house_all(db)
    zzim_list = hobbang_crud_test.get_zzim_list_all(db)
    click = hobbang_crud_test.get_click_list_all(db)

    # 2. 모델 학습     
    result = train_ml_gu(map.user_id, map.user_gu, all_user, all_house, zzim_list, click, db)
    
    # return {'result' : result}


# def train_latlng(map: schemas.MapZoom, db: Session = Depends(get_db)):
#     # 1. data 확인
#     all_user = hobbang_crud_test.get_users(db)
#     all_house = hobbang_crud_test.get_house_all(db)
#     zzim_list = hobbang_crud_test.get_zzim_list(db)
#     click = hobbang_crud_test.get_click_list_all(db)

#     # 2. 모델 학습     
#     result = train_ml_latlng(map.user_id, 
#                             map.min_lat,
#                             map.max_lat,
#                             map.min_lng,
#                             map.max_lng, all_user, all_house, zzim_list, click, db)
    
#     # return {'result' : result}


# @router.post("/inference")
def inference(map: schemas.Items, db: Session = Depends(get_db)):
    # 1. interaction data
    # zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    # click = hobbang_crud_test.get_user_click_list(map.user_id, db)
    
    zzim_list = hobbang_crud_test.get_zzim_list_all(db)
    click = hobbang_crud_test.get_click_list_all(db)


    # 2. 모델 inference
    result1, result2, result3 = inference_ml(map.user_id, zzim_list, click, db)
    result = []
    # print(set(result1))
    for u,i,s in zip(result1, result2, result3):
        if u==map.user_id:
            result.append(i)
            # print(u,i,s)
    # house_ranking = inference_gu(map.user_id, map.user_gu, db)
    house_ranking = []
    if len(result)==0:
        return {'message' : '해당 지역(구)에서 추천할 수 없습니다. 지역 내 찜 목록이 5개 이상인지 확인해주세요.'}
    else:
        for i in range(len(result)):
            house_ranking.append({"house_id": result[len(result)-i-1], "ranking": i+1})

    # 3. house_info 가져오기
    map.house_ranking = {f'{house["house_id"]}': house["ranking"] for house in house_ranking}
    houses = hobbang_crud_test.get_houses_info(map, db,is_ai_recommend=True)

    # 4. 랭킹순으로 정렬(house_list[ranking] = house_info)
    houses = dict(sorted({idx+1: houses[house] for idx,house in enumerate(houses)}.items()))

    return {"houses": houses, "house_id": result}


@router.post("/")
def checkZzimLength(map: schemas.Items, db: Session = Depends(get_db)):
    zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    zzim = [zzim[0] for zzim in zzim_list]
    house_gu_all = hobbang_crud_test.get_house_gu(map.user_gu, db)
    house_gu = [h_gu[0] for h_gu in house_gu_all]
    zzim_gu = []
    for z in zzim:
        if z in house_gu:
            zzim_gu.append(z)
    if len(zzim_gu) < 5:
        return {'code':0,'message' : '해당 지역(구)에서 찜 목록이 부족합니다.'}
    else:
        result = recommendML(map, db)
        sim_score = compare_similarity(zzim_gu, result['house_id'], map, db)
        print("sim_score : ", round(sim_score,4))
        return {
                'code' : 1,
                'message' : '추천을 시작합니다.',
                'sim_score' : round(sim_score,4),
                'houses' : result['houses']
                }


# @router.post("/rec_gu")
def recommendML(map: schemas.Items, db: Session = Depends(get_db)):
    start = time.time()
    train_gu(map, db)
    result = inference(map, db)
    end = time.time()
    print(end-start)
    return result


def compare_similarity(zzim_id, infer_id, map: schemas.Items, db: Session = Depends(get_db)):
    sim_score = compare(map.user_id, zzim_id, infer_id, db)
    return sim_score
