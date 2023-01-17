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
def get_houses_gu(map: schemas.Inference, db: Session):
    # house_scores: Dict(ex: house_scores[house_id] = score)
    house_ids = list(map.house_ranking.keys())
    s = f"""
    SELECT H.*,
        I1.infra_id as id_01, I1.infra_dist as dist_01, I1.infra_cnt as cnt_01, I1.lat as lat_01, I1.lng as lng_01,
        I2.infra_id as id_02, I2.infra_dist as dist_02, I2.infra_cnt as cnt_02, I2.lat as lat_02, I2.lng as lng_02,
        I3.infra_id as id_03, I3.infra_dist as dist_03, I3.infra_cnt as cnt_03, I3.lat as lat_03, I3.lng as lng_03,
        I4.infra_id as id_04, I4.infra_dist as dist_04, I4.infra_cnt as cnt_04, I4.lat as lat_04, I4.lng as lng_04,
        I5.infra_id as id_05, I5.infra_dist as dist_05, I5.infra_cnt as cnt_05, I5.lat as lat_05, I5.lng as lng_05,
        (CASE 
            WHEN(SELECT COUNT(*)
                    FROM hobbang_test.USER_ZZIM Z
                WHERE Z.user_id = {map.user_id}
                    AND H.house_id = Z.house_id) > 0
            THEN 'Y'
            ELSE 'N'
        END) zzim
    FROM hobbang_test.HOUSE_INFO H,
        (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '01'
            ) I1,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '02'
            ) I2,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '03'
            ) I3,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '04'
            ) I4,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '05'
            ) I5
    WHERE 1=1
        AND H.house_id in ({", ".join(house_ids)})
        AND H.local2 = "{map.user_gu}"
     	AND H.grid_id = I1.grid_id
     	AND H.grid_id = I2.grid_id
     	AND H.grid_id = I3.grid_id
     	AND H.grid_id = I4.grid_id
     	AND H.grid_id = I5.grid_id
    """
    return db.execute(s).all()


def get_houses_zoom(map_zoom: schemas.MapZoom, db: Session):
    # house_scores: Dict(ex: house_scores[house_id] = score)
    house_ids = list(map_zoom.house_ranking.keys())
    s = f"""
    SELECT H.*,
        I1.infra_id as id_01, I1.infra_dist as dist_01, I1.infra_cnt as cnt_01, I1.lat as lat_01, I1.lng as lng_01,
        I2.infra_id as id_02, I2.infra_dist as dist_02, I2.infra_cnt as cnt_02, I2.lat as lat_02, I2.lng as lng_02,
        I3.infra_id as id_03, I3.infra_dist as dist_03, I3.infra_cnt as cnt_03, I3.lat as lat_03, I3.lng as lng_03,
        I4.infra_id as id_04, I4.infra_dist as dist_04, I4.infra_cnt as cnt_04, I4.lat as lat_04, I4.lng as lng_04,
        I5.infra_id as id_05, I5.infra_dist as dist_05, I5.infra_cnt as cnt_05, I5.lat as lat_05, I5.lng as lng_05,
        (CASE 
            WHEN(SELECT COUNT(*)
                    FROM hobbang_test.USER_ZZIM Z
                WHERE Z.user_id = {map_zoom.user_id}
                    AND H.house_id = Z.house_id) > 0
            THEN 'Y'
            ELSE 'N'
        END) zzim
    FROM hobbang_test.HOUSE_INFO H,
        (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '01'
            ) I1,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '02'
            ) I2,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '03'
            ) I3,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '04'
            ) I4,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.lat, I.lng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '05'
            ) I5
    WHERE 1=1
        AND H.house_id in ({", ".join(house_ids)})
     	AND H.grid_id = I1.grid_id
     	AND H.grid_id = I2.grid_id
     	AND H.grid_id = I3.grid_id
     	AND H.grid_id = I4.grid_id
     	AND H.grid_id = I5.grid_id
        AND H.lat >= {map_zoom.min_lat}
        AND H.lat <= {map_zoom.max_lat}
        AND H.lng >= {map_zoom.min_lng}
        AND H.lng <= {map_zoom.max_lng}
    """
    return db.execute(s).all()


def write_click_log(user: schemas.ClickLog, db: Session):
    db_click = LogClick(
                    user_id=user.user_id,
                    item_id=user.house_id,
                    log_type=user.log_type
                )
    db.add(db_click)
    db.commit()
    db.refresh(db_click)
    return db_click


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