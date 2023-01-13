from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from crud import hobbang_crud_test
# from apis import test # main logic

router = APIRouter(
    prefix="/map", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리


# 맵 화면 진입시 요청되는 api
@router.get("/") # Route Path
def getHousesGu(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 맵 zoom in/out 했을 때 요청되는 api
@router.get("/") # Route Path
def getHousesZoom(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 구 변화했을 때 요청되는 api
@router.get("/") # Route Path
def changeGu(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}