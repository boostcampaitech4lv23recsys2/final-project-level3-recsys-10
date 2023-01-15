# crud/hobbang_crud_test.py

from sqlalchemy.orm import Session
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick

# map
def get_user_by_user_id(user_id, db: Session):
    return db.query(UsersInfo).filter_by(user_id=user_id).one()

def get_infra_by_user_id(user_id, db: Session):
    return db.query(UsersInfra.infra_type).filter_by(user_id=user_id, infra_yn='Y').all()

def get_houses_gu(gu, db: Session):
    return db.query(HouseInfo).filter_by(sold_yn = 'N', local2 = gu).all()

# def get_houses_zoom(db: Session, min_lat, min_lng, max_lat, max_lng):
#     return db.query(HousesInfo).filter_by()

def get_infra(db: Session):
    return db.query(Infra).all()



