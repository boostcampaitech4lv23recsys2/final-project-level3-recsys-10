from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from crud.schemas import getHousesList
from crud import hobbang_crud_test, schemas
from recommend.rule_based import inference_gu, inference_latlng

# import os
# print(os.getcwd())
# import sys
# # sys.path.insert(0, '/home/user/PROJECT_DIR/')
# sys.path.append('../../../modeling')
# print(sys.path)
# from apis import test # main logic

router = APIRouter(
    prefix="/map", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리


# 맵 화면 진입시 요청되는 api
# request: user_id, user_gu
@router.post("/items")
def getHouses(map: schemas.Inference, db: Session = Depends(get_db)):
    # 1. user_id 로 USERS_INFRA.infra_type(infra_yn='Y')
    # infra = hobbang_crud_test.get_infra_by_user_id(map.user_id, db)
    # infra_list = [i.infra_type for i in infra]

    # 2. 모델 inference
    house_ranking = inference_gu(map.user_id, map.user_gu, db)
    map.house_ranking = {f'{house["house_id"]}': house["ranking"] for house in house_ranking}

    # 3. house 목록
    res = hobbang_crud_test.get_houses_gu(map, db)
    
    return {
        # "res": res,
        # "house_ranking": map.house_ranking,  # inference result
        "houses": getHousesList(map, res)
    }


# 맵 zoom in/out 했을 때 요청되는 api(infernece 포함)
# request: user_id, lat/lng(최대, 최소)
@router.post("/items/zoom")
def getHousesZoom(map: schemas.MapZoom, db: Session = Depends(get_db)):
    # 1. user_id 로 USERS_INFRA.infra_type(infra_yn='Y')
    # infra = hobbang_crud_test.get_infra_by_user_id(map.user_id, db)
    # infra_list = [i.infra_type for i in infra]

    # 2. 모델 inference
    house_ranking = inference_latlng(map.user_id,
                                    map.min_lat,
                                    map.max_lat,
                                    map.min_lng,
                                    map.max_lng, db)
    map.house_ranking = {f'{house["house_id"]}': house["ranking"] for house in house_ranking}

    # 3. house 목록
    res = hobbang_crud_test.get_houses_gu(map, db)
    
    return {
        # "res": res,
        # "house_ranking": map.house_ranking,  # inference result
        "houses": getHousesList(map, res)
    }


# 매물 클릭시 요청되는 api
# request: user_id, house_id, log_type
@router.post("/itemd/click")
def WriteClickLog(map: schemas.ClickLog, db: Session = Depends(get_db)):
    res = hobbang_crud_test.write_click_log(map, db)

    return {
        "res": res
    }


# # 맵 zoom in/out 했을 때 요청되는 api(infernece 없음)
# # request: 위도, 경도(최대, 최소)
# @router.post("/items/zoom")
# def getHousesZoom(map_zoom: schemas.MapZoom, db: Session = Depends(get_db)):
#     res = hobbang_crud_test.get_houses_zoom(map_zoom, db)
    
#     return {
#         "res": res,
#         "house_ranking": map_zoom.house_ranking,  # inference result
#         # "grid": [map_zoom.min_lat, map_zoom.min_lng, map_zoom.max_lat, map_zoom.max_lng], 
#         "houses": getHousesList(map_zoom, res)
#     }
