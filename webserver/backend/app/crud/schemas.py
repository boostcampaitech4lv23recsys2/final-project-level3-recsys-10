from typing import List, Union, Optional, Dict, Any
from sqlalchemy import CHAR
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class UserBase(BaseModel):
    """
    description: 유저 한 명에 대한 정보
    """
    user_id: int = Field(None) 
    name: str = Field(None)
    pw: str = Field(None)

class UserCreate(UserBase):
    """
    despription: 새로운 유저 추가
    application: 회원가입
    """
    # user_id: int = Field(None) # UUID = Field(default_factory=uuid4)
    # pw: str = Field(None)
    user_gu: str = Field(None)
    user_age: int = Field(None)
    user_sex: int = Field(None)
    user_type: str = Field(None)

class UserSelect(BaseModel):
    # user_id
    user_id: int = Field(None)
    user_type: str = Field(None)
    user_gu: str = Field(None)
    infra: list = Field(None)
    register_date: datetime = Field(None)

class Inference(BaseModel):
    user_id: int = Field(None)
    user_gu: str = Field(None)
    house_ranking: Dict = Field(None) # inference 결과 저장할 때 필요

class MapZoom(Inference):
    min_lat: float = Field(None)
    min_lng: float = Field(None)
    max_lat: float = Field(None)
    max_lng: float = Field(None)

def getHousesList(map_zoom, res):
    return sorted([{map_zoom.house_ranking[f'{r.house_id}']: 
                        {"house_id": r.house_id,
                        "lat": r.lat,
                        "lng": r.lng,
                        "grid_id": r.grid_id,
                        "ranking": map_zoom.house_ranking[f'{r.house_id}'],
                        "zzim": r.zzim,
                        "information" : {
                            "local1": r.local1,
                            "local2": r.local2,
                            "sales_type": r.sales_type,
                            "service_type": r.service_type,
                            "price_sales": r.price_sales,
                            "price_deposit": r.price_deposit,
                            "price_monthly_rent": r.price_monthly_rent,
                            "floor": r.floor,
                            "floor_total": r.floor_total,
                            "manage_cost": r.manage_cost,
                            "room_cnt": r.room_cnt,
                            "bathroom_cnt": r.bathroom_cnt,
                            },
                        "related_infra":{
                            "01" : {
                                "nearest_distance": r.dist_01,
                                "nearest_lat": r.lat_01,
                                "nearest_lng" : r.lng_01,
                                "cnt": r.cnt_01
                            },
                            "02" : {
                                "nearest_distance": r.dist_02,
                                "nearest_lat": r.lat_02,
                                "nearest_lng" : r.lng_02,
                                "cnt": r.cnt_02
                            },
                            "03" : {
                                "nearest_distance": r.dist_03,
                                "nearest_lat": r.lat_03,
                                "nearest_lng" : r.lng_03,
                                "cnt": r.cnt_03
                            },
                            "04" : {
                                "nearest_distance": r.dist_04,
                                "nearest_lat": r.lat_04,
                                "nearest_lng" : r.lng_04,
                                "cnt": r.cnt_04
                            },
                            "05" : {
                                "nearest_distance": r.dist_05,
                                "nearest_lat": r.lat_05,
                                "nearest_lng" : r.lng_05,
                                "cnt": r.cnt_05
                            },
                            "06" : {
                                "nearest_distance": r.dist_06,
                                "nearest_lat": r.lat_06,
                                "nearest_lng" : r.lng_06,
                                "cnt": r.cnt_06
                            },
                            "07" : {
                                "nearest_distance": r.dist_07,
                                "nearest_lat": r.lat_07,
                                "nearest_lng" : r.lng_07,
                                "cnt": r.cnt_07
                            }
                        }
                        } for r in res}])

class ClickLog(BaseModel):
    user_id: int = Field(None)
    house_id: int = Field(None)
    log_type: str = Field(None)

class ClickZzim(BaseModel):
    user_id: int = Field(None)
    house_id: int = Field(None)