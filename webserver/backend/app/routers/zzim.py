from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from db.connection import get_db
from crud import hobbang_crud_test, schemas
from db.models import hobbang_model
# from apis import test # main logic

from datetime import datetime

router = APIRouter(
    prefix="/zzim", # url 앞에 고정적으로 붙는 경로추가
) # Route 분리


# 찜목록 조회시 요청되는 api
@router.get("/items/{user_id}") # Route Path
def getZzimList(user_id, db: Session = Depends(get_db)):
    res = hobbang_crud_test.get_zzim_list(user_id, db)
    
    return res


# 찜등록시 요청되는 api
@router.post("/items/register/") # Route Path
def makeZzim(zzim: schemas.ClickLog, db: Session = Depends(get_db)):
    res = hobbang_crud_test.check_item(zzim.house_id, db)
    if res==0:
        res = hobbang_crud_test.write_zzim_log(zzim, db)
        return {
            "messege" : f"{zzim.house_id} 매물이 찜 목록에 추가되었습니다.",
            "zzim_list"  : res,
            }
    else:
        return {
            "messege" : "이미 찜 목록에 존재하는 매물입니다."
        } 

        
# # 찜등록시 요청되는 api
# @router.get("/{user_id}/make/{house_id}}") # Route Path
# def makeZzim(user_id, house_id, db: Session = Depends(get_db)):
#     zzim = getZzimList(user_id, db)
#     zzim_list = [z.house_id for z in zzim]
    
#     if int(house_id) in zzim_list:
#         return {
#             "messege" : "이미 찜 목록에 존재하는 매물입니다."
#         }
#     else:
#         max_idx_before = db.query(func.max(hobbang_model.UserZzim.idx)).scalar()
#         if max_idx_before==None:
#             max_idx_before=0
        
#         db_zzim = hobbang_model.UserZzim(
#             idx=int(max_idx_before + 1),
#             user_id=user_id,
#             house_id=house_id,
#             zzim_date=datetime.now()
#             )
#         db.add(db_zzim)
#         db.commit()
#         db.refresh(db_zzim)
#         return {
#             "messege" : f"{house_id} 매물이 찜 목록에 추가되었습니다.",
#             "zzim_list"  : res,
#             }

        
# 찜등록 취소시 요청되는 api
@router.post("/items/unregister/") # Route Path
def deleteZzim(zzim: schemas.ClickLog, db: Session = Depends(get_db)):
    res = hobbang_crud_test.check_item(zzim.house_id, db)
    
    if res==0:
        return {
            "message" : "삭제할 매물이 없습니다.",
        }
    else:
        house_id = hobbang_crud_test.delete_zzim_log(zzim, db)
        return {
            "message" : f"{house_id} 매물이 삭제되었습니다.",
	    }
        
        
# # 찜등록 취소시 요청되는 api
# @router.get("/{user_id}/delete/{house_id}}") # Route Path
# def deleteZzim(user_id, house_id, db: Session = Depends(get_db)):
#     zzim = getZzimList(user_id, db)
#     zzim_list = [z.house_id for z in zzim]
    
#     if int(house_id) in zzim_list:
#         db.query(hobbang_model.UserZzim).filter(hobbang_model.UserZzim.house_id==house_id).delete(synchronize_session=False)
#         db.commit()
        
#         return {
#             "message" : f"{house_id} 매물이 삭제되었습니다.",
# 	    }
#     else:
#         return {
#             "message" : "삭제할 매물이 없습니다.",
#         }
