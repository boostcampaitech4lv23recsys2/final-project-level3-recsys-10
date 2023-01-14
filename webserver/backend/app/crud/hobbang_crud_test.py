# crud/hobbang_crud_test.py

from sqlalchemy.orm import Session
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick
from db.models import hobbang_model
from . import schemas

def get_infra(db: Session):
    return db.query(HouseInfo).filter_by(house_id=1).all()

def get_user_by_user_id(user_id, db: Session):
    return db.query(UsersInfo).filter_by(user_id=user_id).one()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.pw + "notreallyhashed"    
    # max_id_before = db.query(func.max(hobbang_model.UsersInfo.user_id)).scalar()
    db_user = hobbang_model.UsersInfo(
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