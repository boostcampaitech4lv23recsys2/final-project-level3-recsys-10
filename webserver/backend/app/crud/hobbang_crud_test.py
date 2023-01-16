# crud/hobbang_crud_test.py

from sqlalchemy.orm import Session
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick
from . import schemas

######### common
def get_user_by_user_id(user_id, db: Session):
    return db.query(UsersInfo).filter_by(user_id=user_id).one()

def get_infra_by_user_id(user_id, db: Session):
    return db.query(UsersInfra.infra_type).filter_by(user_id=user_id, infra_yn='Y').all()

def get_infra(db: Session):
    return db.query(HouseInfo).filter_by(house_id=1).all()


######### map
def get_houses_gu(gu, db: Session):
    return db.query(HouseInfo).filter_by(sold_yn = 'N', local2 = gu).all()

def get_houses_zoom(map_zoom: schemas.MapZoom, db: Session):
    # house_scores: Dict(ex: house_scores[house_id] = score)
    house_ids = list(map_zoom.house_scores.keys())
    # 형변환 문제
    return db.query(HouseInfo).filter(
        HouseInfo.house_id.in_(house_ids),
        HouseInfo.lat >= map_zoom.min_lat,
        HouseInfo.lat <= map_zoom.max_lat,
        HouseInfo.lng >= map_zoom.min_lng,
        HouseInfo.lng <= map_zoom.max_lng
    ).all() # score별로 정렬 필요


######### users
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.pw + "notreallyhashed"    
    # max_id_before = db.query(func.max(hobbang_model.UsersInfo.user_id)).scalar()
    db_user = UsersInfo(
                    # user_id=int(max_id_before + 1), 
                    pw=fake_hashed_password, 
                    name=user.name,
                    user_gu = user.user_gu,
                    user_age=user.user_age,
                    user_sex=user.user_sex, 
                    user_type = user.user_type
                )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def check_user_name(name, db: Session):
    return db.query(UsersInfo).filter_by(name = name).count()

def get_users(db: Session):
    return db.query(UsersInfo).all()


######### zzim
def get_zzim_list(user_id, db: Session):
    s = f"""
    SELECT * FROM hobbang_test.USER_ZZIM
    WHERE USER_ZZIM.user_id={user_id}
    """
    return db.execute(s).all()