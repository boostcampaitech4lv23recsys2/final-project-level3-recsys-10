# crud/hobbang_crud_test.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models.hobbang_model import HouseInfo, UsersInfo, UsersInfra, UserZzim, Infra, InfraInfo, Grid, GridScore, LogClick
from . import schemas
from datetime import datetime
from collections import defaultdict

######### common
def get_user_by_user_id(user_id, db: Session):
    return db.query(UsersInfo).filter_by(user_id=user_id).one()

def get_infra_by_user_id(user_id, db: Session):
    return db.query(UsersInfra.infra_type).filter_by(user_id=user_id, infra_yn='Y').all()

# def get_infra(db: Session):
#     return db.query(HouseInfo).filter_by(house_id=1).all()


######### map
def get_houses_gu(map: schemas.Inference, db: Session):
    # house_scores: Dict(ex: house_scores[house_id] = score)
    house_ids = list(map.house_ranking.keys())
    if not house_ids:
        return {}
    s = f"""
    SELECT H.*,
        I1.infra_id as id_01, I1.infra_dist as dist_01, I1.infra_cnt as cnt_01, ST_X(I1.latlng) as lat_01, ST_Y(I1.latlng) as lng_01,
        I2.infra_id as id_02, I2.infra_dist as dist_02, I2.infra_cnt as cnt_02, ST_X(I2.latlng) as lat_02, ST_Y(I2.latlng) as lng_02,
        I3.infra_id as id_03, I3.infra_dist as dist_03, I3.infra_cnt as cnt_03, ST_X(I3.latlng) as lat_03, ST_Y(I3.latlng) as lng_03,
        I4.infra_id as id_04, I4.infra_dist as dist_04, I4.infra_cnt as cnt_04, ST_X(I4.latlng) as lat_04, ST_Y(I4.latlng) as lng_04,
        I5.infra_id as id_05, I5.infra_dist as dist_05, I5.infra_cnt as cnt_05, ST_X(I5.latlng) as lat_05, ST_Y(I5.latlng) as lng_05,
        --I6.infra_id as id_06, I6.infra_dist as dist_06, I6.infra_cnt as cnt_06, ST_X(I6.latlng) as lat_06, ST_Y(I6.latlng) as lng_06,
        --I7.infra_id as id_07, I7.infra_dist as dist_07, I7.infra_cnt as cnt_07, ST_X(I7.latlng) as lat_07, ST_Y(I7.latlng) as lng_07,
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
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '01'
            ) I1,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '02'
            ) I2,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '03'
            ) I3,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '04'
            ) I4,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '05'
            ) I5,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '06'
            ) I6,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '07'
            ) I7
    WHERE 1=1
        AND H.house_id in ({", ".join(house_ids)})
        AND H.local2 = "{map.user_gu}"
     	AND H.grid_id = I1.grid_id
     	AND H.grid_id = I2.grid_id
     	AND H.grid_id = I3.grid_id
     	AND H.grid_id = I4.grid_id
     	AND H.grid_id = I5.grid_id
        AND H.grid_id = I6.grid_id
        AND H.grid_id = I7.grid_id
    """
    return db.execute(s).all()


def get_houses_zoom(map_zoom: schemas.MapZoom, db: Session):
    # house_scores: Dict(ex: house_scores[house_id] = score)
    house_ids = list(map_zoom.house_ranking.keys())
    if not house_ids:
        return {}
    s = f"""
    SELECT H.*,
        I1.infra_id as id_01, I1.infra_dist as dist_01, I1.infra_cnt as cnt_01, ST_X(I1.latlng) as lat_01, ST_Y(I1.latlng) as lng_01,
        I2.infra_id as id_02, I2.infra_dist as dist_02, I2.infra_cnt as cnt_02, ST_X(I2.latlng) as lat_02, ST_Y(I2.latlng) as lng_02,
        I3.infra_id as id_03, I3.infra_dist as dist_03, I3.infra_cnt as cnt_03, ST_X(I3.latlng) as lat_03, ST_Y(I3.latlng) as lng_03,
        I4.infra_id as id_04, I4.infra_dist as dist_04, I4.infra_cnt as cnt_04, ST_X(I4.latlng) as lat_04, ST_Y(I4.latlng) as lng_04,
        I5.infra_id as id_05, I5.infra_dist as dist_05, I5.infra_cnt as cnt_05, ST_X(I5.latlng) as lat_05, ST_Y(I5.latlng) as lng_05,
        I6.infra_id as id_06, I6.infra_dist as dist_06, I6.infra_cnt as cnt_06, ST_X(I6.latlng) as lat_06, ST_Y(I6.latlng) as lng_06,
        I7.infra_id as id_07, I7.infra_dist as dist_07, I7.infra_cnt as cnt_07, ST_X(I7.latlng) as lat_07, ST_Y(I7.latlng) as lng_07,
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
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '01'
            ) I1,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '02'
            ) I2,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '03'
            ) I3,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '04'
            ) I4,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '05'
            ) I5,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '06'
            ) I6,
            (SELECT G.infra_id, G.infra_dist, G.infra_cnt, G.grid_id,
                I.latlng
            FROM hobbang_test.GRID_SCORE G,
                    hobbang_test.INFRA_INFO I
            WHERE G.infra_id = I.infra_id
                AND G.infra_type = '07'
            ) I7
    WHERE 1=1
        AND H.house_id in ({", ".join(house_ids)})
     	AND H.grid_id = I1.grid_id
     	AND H.grid_id = I2.grid_id
     	AND H.grid_id = I3.grid_id
     	AND H.grid_id = I4.grid_id
     	AND H.grid_id = I5.grid_id
        AND H.grid_id = I6.grid_id
        AND H.grid_id = I7.grid_id
        AND ST_CONTAINS(ST_POLYFROMTEXT('POLYGON(({map_zoom.min_lat} {map_zoom.min_lng}
                                                , {map_zoom.min_lat} {map_zoom.max_lng}
                                                , {map_zoom.max_lat} {map_zoom.max_lng}
                                                , {map_zoom.max_lat} {map_zoom.min_lng}
                                                , {map_zoom.min_lat} {map_zoom.min_lng}))')
                                        , H.latlng)
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
    #fake_hashed_password = user.pw + "notreallyhashed"    
    # max_id_before = db.query(func.max(hobbang_model.UsersInfo.user_id)).scalar()
    db_user = UsersInfo(
                    # user_id=int(max_id_before + 1), 
                    pw=user.pw, 
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

def login_user(user: schemas.UserBase, db: Session):
    #return db.query(UsersInfo).filter_by(name = user.name, pw = user.pw).first()
    return db.query(UsersInfo).filter_by(name = user.name).first()

def create_user_infra(user: schemas.UserSelect, db: Session):
    
    infra_list = defaultdict(int)
    
    for inf_type in user.infra: 
        infra_list[inf_type]+=1
    
    s = f"""
    INSERT INTO hobbang_test.USERS_INFRA(user_id, infra_type, infra_yn, register_date, update_date)
	    VALUES ({user.user_id}, '01', IF({infra_list["01"]}=0, "N", "Y"), now(), now())
                ,({user.user_id}, '02', IF({infra_list["02"]}=0, "N", "Y"), now(), now())
                ,({user.user_id}, '03', IF({infra_list["03"]}=0, "N", "Y"), now(), now())
                ,({user.user_id}, '04', IF({infra_list["04"]}=0, "N", "Y"), now(), now())
                ,({user.user_id}, '05', IF({infra_list["05"]}=0, "N", "Y"), now(), now())
                ,({user.user_id}, '06', IF({infra_list["06"]}=0, "N", "Y"), now(), now())
                ,({user.user_id}, '07', IF({infra_list["07"]}=0, "N", "Y"), now(), now())
    """
    
    # s = f"""
    # DROP PROCEDURE IF EXISTS loopInsert;
    # CREATE PROCEDURE loopInsert()
    # BEGIN
    #     DECLARE i INT DEFAULT 1;
    #     WHILE i <= 7
    #         DO
    #             INSERT INTO hobbang_test.USERS_INFRA(user_id,infra_type,infra_yn,register_date,update_date)
    #             VALUES (, CONCAT('0',CHAR(i)), );
    #             SET i = i + 1;
    #         END WHILE;
    # END;
    # CALL loopInsert();
    # """
    
    # 인프라 총 7개 
    # infra_types = {'subway':'01','cs':'02','mart':'03','park':'04','cafe':'05','phar':'06','theater':'07'}
    
    # for inf_type in infra_types.values() :
    #     db_user_infra = UsersInfra(
    #                     # idx : auto_increase
    #                     # user_id = db.query(UsersInfo).filter_by(user_id=user.user_id).one().user_id,
    #                     user_id = user.user_id,
    #                     infra_type= inf_type,
    #                     infra_yn = 'Y' if inf_type in user.infra  else 'N',
    #                     register_date = user.register_date,
    #                     update_date = datetime.now()
    #                 )
    #     db.add(db_user_infra)
    #     db.commit()
    #     db.refresh(db_user_infra)
    # return db_user_infra
    db.execute(s)
    db.commit()
    return 1


def update_user_gu(user: schemas.UserSelect, db: Session):
    user_info = db.query(UsersInfo).filter(UsersInfo.user_id == user.user_id).first()
    user_info.user_gu = user.user_gu
    db.commit()
    return 1


######### zzim
def get_zzim_list(user_id, db: Session):
    s = f"""
    SELECT * FROM hobbang_test.USER_ZZIM
    WHERE USER_ZZIM.user_id={user_id}
    """
    return db.execute(s).all()
