from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from crud import hobbang_crud_test
from crud import crud_test

from db.models import hobbang_model
# from apis import test # main logic

router = APIRouter(
    prefix="/users", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리


# 회원가입 시 요청되는 api
@router.post("/") # Route Path
def createUser(users:hobbang_crud_test.UserCreate, db: Session = Depends(get_db)):
    res = hobbang_crud_test.create_user(db,users)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    print( res)
    
    return {
        "res" : res
	}

# 닉네임 중복확인 시 요청되는 api
@router.get("/") # Route Path
def checkName(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 로그인 시 요청되는 api
@router.get("/") # Route Path
def loginUser(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 비회원이 인프라 선택시 요청되는 api
@router.get("/") # Route Path
def selectInfra(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}


# 회원이 인프라 선택시 요청되는 api
@router.get("/") # Route Path
def selectInfraUser(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}