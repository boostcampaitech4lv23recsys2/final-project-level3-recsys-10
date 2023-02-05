import random
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db

from crud import hobbang_crud_test, schemas
from recommend.rule_based import inference_gu, inference_latlng
from recommend.ML import train_ml_gu, train_ml_latlng, inference_ml

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
    zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    click = hobbang_crud_test.get_click_list(db)

    # 2. 모델 학습     
    result = train_ml_gu(map.user_id, map.user_gu, all_user, all_house, zzim_list, click, db)
    
    # return {'result' : result}


def train_latlng(map: schemas.MapZoom, db: Session = Depends(get_db)):
    # 1. data 확인
    all_user = hobbang_crud_test.get_users(db)
    all_house = hobbang_crud_test.get_house_all(db)
    zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    click = hobbang_crud_test.get_click_list(db)

    # 2. 모델 학습     
    result = train_ml_latlng(map.user_id, 
                            map.min_lat,
                            map.max_lat,
                            map.min_lng,
                            map.max_lng, all_user, all_house, zzim_list, click, db)
    
    # return {'result' : result}


# @router.post("/inference")
def inference(map: schemas.Items, db: Session = Depends(get_db)):
    # 1. interaction data
    zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    click = hobbang_crud_test.get_user_click_list(map.user_id, db)
    
    # 2. 모델 inference
    result = inference_ml(zzim_list, click, db)

    house_ranking = inference_gu(map.user_id, map.user_gu, db)
    house_ranking.append({"house_id": result[0], "ranking": 0})

    # 3. house_info 가져오기
    map.house_ranking = {f'{house["house_id"]}': house["ranking"] for house in house_ranking}
    houses = hobbang_crud_test.get_houses_info(map, db)

    # 4. 랭킹순으로 정렬(house_list[ranking] = house_info)
    houses = dict(sorted({houses[house]["ranking"]: houses[house] for house in houses}.items()))

    return {"houses": houses}


@router.post("/rec_gu")
def recommend_ML(map: schemas.Items, db: Session = Depends(get_db)):
    start = time.time()
    train_gu(map, db)
    result = inference(map, db)
    end = time.time()
    print(end-start)
    return result


@router.post("/rec_latlng")
def recommend_ML(map: schemas.MapZoom, db: Session = Depends(get_db)):
    start = time.time()
    train_latlng(map, db)
    result = inference(map, db)
    end = time.time()
    print(end-start)
    return result