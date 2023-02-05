import random
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db

from crud import hobbang_crud_test, schemas
from recommend.rule_based import inference_gu, inference_latlng
from recommend.ML import train_ml, inference_ml

# from modeling.RecBole import run_recbole

# from modeling.RecBole.recbole.properties
import sys
import os

router = APIRouter(
    prefix="/recommend",
)

@router.post("/train")
def train(map: schemas.Items, db: Session = Depends(get_db)):
    all_user = hobbang_crud_test.get_users(db)
    all_house = hobbang_crud_test.get_house_all(db)
    zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    # zzim_list = hobbang_crud_test.get_zzim_list(map.user_id, db)
    # click = hobbang_crud_test.get_user_click_list(map.user_id, db)
    click = hobbang_crud_test.get_click_list(db)
    # print(all_house)
    
    result = train_ml(map.user_id, all_user, all_house, zzim_list, click, db)
    
    return {'result' : result}


@router.post("/inference")
def inference(map: schemas.Items, db: Session = Depends(get_db)):
    zzim_list = hobbang_crud_test.get_user_zzim_list(map.user_id, db)
    click = hobbang_crud_test.get_user_click_list(map.user_id, db)
    
    result = inference_ml(zzim_list, click, db)
    
    return {'result' : result}