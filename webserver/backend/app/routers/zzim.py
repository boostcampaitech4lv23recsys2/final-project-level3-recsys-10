from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from crud import hobbang_crud_test
# from apis import test # main logic

router = APIRouter(
    prefix="/zzim", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리


# 찜등록시 요청되는 api
@router.get("/") # Route Path
def makeZzim(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 찜목록 조회시 요청되는 api
@router.get("/") # Route Path
def getZzimList(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 찜등록 취소시 요청되는 api
@router.get("/") # Route Path
def deleteZzim(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}