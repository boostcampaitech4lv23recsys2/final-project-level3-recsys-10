from typing import Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from crud import hobbang_crud_test, schemas

# from apis import test # main logic

router = APIRouter(
    prefix="/users", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리


# 회원가입 시 요청되는 api
# 닉네임, 나이 성별 지역 비번
@router.post("/createuser/", response_model=schemas.UserCreate) # Route Path
def createUser(user: schemas.UserCreate, db: Session = Depends(get_db)):
    res = hobbang_crud_test.create_user(db, user)  # get_infra(db): INFRA 테이블 조회(임시)
    return {
        "res": res
    }

# # 회원가입
# @app.post("/register", response_model=schemas.User)
# def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_id(db, user_id=user.user_id)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Error 발생!")
#     return crud.create_user(db=db, user=user)


# 닉네임 중복확인 시 요청되는 api
@router.get("/checkname/{name}") # Route Path
def checkName(name, db: Session = Depends(get_db)):
    res = hobbang_crud_test.check_user_name(name, db)  # get_infra(db): INFRA 테이블 조회(임시)
    if res == 0:
        return {
            "res": "사용할 수 있는 이름입니다"
        }
    else:
        return {
            "res": "중복된 이름이 있습니다"
        }


# 로그인 시 요청되는 api
@router.post("/login/") # Route Path
def loginUser(user: schemas.UserBase, db: Session = Depends(get_db)):
    res = hobbang_crud_test.login_user(user, db)  # get_infra(db): INFRA 테이블 조회(임시)
    if res:
        return {
            "msg": "로그인에 성공했습니다.",
            "user_id": res.user_id,
            "user_gu": res.user_gu,

        }
    else:
        return {
            "msg": "아이디 혹은 비밀번호가 일치하지 않습니다.",
            "user_id": "",
            "user_gu": "",
        }




# 비회원/회원이 인프라 선택시 요청되는 api
@router.post("/selectInfras") # Route Path
def selectInfra(UserSelect: schemas.UserSelect, db: Session = Depends(get_db)):
    # request: user_id(비회원이면 null), user_type
    # 0) user: 비회원 > user_id
    user_id = UserSelect.user_id
    user_gu = UserSelect.user_gu
    user_type = UserSelect.user_type
    
    # 1) selected_infra 정보 저장 > user_id, user_gu
    ###### 여기서 쿼리 날려서 infra 정보 저장헤주세요~
    
    res = hobbang_crud_test.create_user_infra(UserSelect, db) # 예시   
    # return {
    #     "res" : res
    # }    
    return {
        "user_id" : user_id,
        "user_gu": user_gu
	}



# 회원이 인프라 선택시 요청되는 api
@router.get("/") # Route Path
def selectInfraUser(db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_infra(db)  # get_infra(db): INFRA 테이블 조회(임시)
    # res = crud_test.get_items(db)
    
    return {
        "res" : res,
	}