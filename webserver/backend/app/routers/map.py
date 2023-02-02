import random
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
# from crud.schemas import getHousesList
from crud import hobbang_crud_test, schemas
from recommend.rule_based import inference_gu, inference_latlng
from recommend.content_based_filtering import inference_gu_CB, inference_latlng_CB

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
def getHouses(map: schemas.Items, db: Session = Depends(get_db)):
    # 1. cold starter 확인(zzim 기록)
    latest_zzim = hobbang_crud_test.get_latest_zzim(map.user_id, db)
    # print(latest_zzim)
    # infra = hobbang_crud_test.get_infra_by_user_id(map.user_id, db)
    # infra_list = [i.infra_type for i in infra]

    # 2. 모델 inference
    house_id = ""
    if latest_zzim:
        house_sim5 = inference_gu_CB(map.user_id, map.user_gu, latest_zzim[0], db)
        # print(house_sim5)
        house_id = random.choice(house_sim5)
        # print(house_id)
    house_ranking = inference_gu(map.user_id, map.user_gu, db)
    house_ranking.append({"house_id": house_id, "ranking": 0})
    
    # 3. house_info 가져오기
    map.house_ranking = {f'{house["house_id"]}': house["ranking"] for house in house_ranking}
    houses = hobbang_crud_test.get_houses_info(map, db)

    # 4. 랭킹순으로 정렬(house_list[ranking] = house_info)
    houses = dict(sorted({houses[house]["ranking"]: houses[house] for house in houses}.items()))
    
    return {
        # "res": res
        # "house_ranking": house_ranking,
        # "house_ranking": map.house_ranking,  # inference result
        "houses": houses
        # "houses": getHousesList(map, res)
    }


# 맵 zoom in/out 했을 때 요청되는 api(infernece 포함)
# request: user_id, lat/lng(최대, 최소)
@router.post("/items/zoom")
def getHousesZoom(map: schemas.MapZoom, db: Session = Depends(get_db)):
    # 1. cold starter 확인(zzim 기록)
    latest_zzim = hobbang_crud_test.get_latest_zzim(map.user_id, db)
    # print(latest_zzim)
    # infra = hobbang_crud_test.get_infra_by_user_id(map.user_id, db)
    # infra_list = [i.infra_type for i in infra]

    # 2. 모델 inference
    house_id = ""
    if latest_zzim:
        house_sim5 = inference_latlng_CB(map.user_id,
                                    map.min_lat,
                                    map.max_lat,
                                    map.min_lng,
                                    map.max_lng, latest_zzim[0], db)
        # print(house_sim5)
        house_id = random.choice(house_sim5)
        # print(house_id)
    house_ranking = inference_latlng(map.user_id,
                                    map.min_lat,
                                    map.max_lat,
                                    map.min_lng,
                                    map.max_lng, db)
    house_ranking.append({"house_id": house_id, "ranking": 0})

    # 3. house_info 가져오기
    map.house_ranking = {f'{house["house_id"]}': house["ranking"] for house in house_ranking}
    houses = hobbang_crud_test.get_houses_info(map, db)

    # 4. 랭킹순으로 정렬(house_list[ranking] = house_info)
    houses = dict(sorted({houses[house]["ranking"]: houses[house] for house in houses}.items()))
    
    return {
        # "res": res
        # "house_ranking": map.house_ranking,  # inference result
        "houses": houses
        # "houses": getHousesList(map, res)
    }


# 매물 클릭시 요청되는 api
# request: user_id, house_id, log_type
@router.post("/items/click")
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
