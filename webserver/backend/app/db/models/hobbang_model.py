# models/test_model.py

from sqlalchemy import Column, String, VARCHAR, CHAR, Integer, BigInteger, Float, DateTime
# from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from db.session import Base


class HouseInfo(Base):
    __tablename__ = "HOUSE_INFO"

    house_id = Column(Integer, primary_key=True)
    zigbang_id = Column(Integer)
    # lat = Column(Float)
    # lng = Column(Float)
    grid_id = Column(Integer)   # Foreign key
    local1 = Column(VARCHAR(20))  # 시
    local2 = Column(VARCHAR(20))  # 구
    latlng = Column(Geometry('POINT', srid=4326))
    sales_type = Column(VARCHAR(255))
    service_type = Column(VARCHAR(255))
    price_sales = Column(Integer)
    price_deposit = Column(Integer)
    price_monthly_rent = Column(Integer)
    floor = Column(Integer)
    floor_total = Column(Integer)
    manage_cost = Column(Integer)
    room_cnt = Column(Integer)
    bathroom_cnt = Column(Integer)
    register_date = Column(DateTime)
    update_date = Column(DateTime)
    sold_yn = Column(CHAR(1))


class UsersInfo(Base):
    __tablename__ = "USERS_INFO"

    user_id = Column(Integer, primary_key=True, index=True)
    pw = Column(String)
    name = Column(String)
    user_gu = Column(String)
    user_age = Column(Integer)
    user_sex = Column(Integer)
    user_type = Column(CHAR)
    register_date = Column(DateTime)
    update_date = Column(DateTime)



class UsersInfra(Base):
    __tablename__ = "USERS_INFRA"

    idx = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    infra_type = Column(CHAR(2))
    infra_yn = Column(CHAR(1))
    register_date = Column(DateTime)
    update_date = Column(DateTime)
    

class UserZzim(Base):
    __tablename__ = "USER_ZZIM"

    idx = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    house_id = Column(Integer)
    zzim_date = Column(DateTime)


class Infra(Base):
    __tablename__ = "INFRA"

    infra_type = Column(CHAR(2), primary_key=True, index=True)
    infra = Column(VARCHAR(255))


class InfraInfo(Base):
    __tablename__ = "INFRA_INFO"

    infra_id = Column(CHAR(20), primary_key=True)
    infra_type = Column(CHAR(2))
    name = Column(VARCHAR(255))
    # lat = Column(Float)
    # lng = Column(Float)
    local1 = Column(VARCHAR(20))
    local2 = Column(VARCHAR(20))
    latlng = Column(Geometry('POINT', srid=4326))
    grid_id = Column(Integer)
    register_date = Column(DateTime)
    update_date = Column(DateTime)
    

class Grid(Base):
    __tablename__ = "GRID"

    grid_id = Column(Integer, primary_key=True)
    min_lat = Column(BigInteger)
    min_lng = Column(BigInteger)
    max_lat = Column(BigInteger)
    max_lng = Column(BigInteger)
    main_lat = Column(BigInteger)
    main_lng = Column(BigInteger)


class GridScore(Base):
    __tablename__ = "GRID_SCORE"

    idx = Column(Integer, primary_key=True, index=True)
    grid_id = Column(Integer)
    infra_type = Column(CHAR(2))
    infra_id = Column(CHAR(8))
    infra_dist = Column(Float)
    infra_cnt = Column(Integer)
    infra_dist_score = Column(Float)
    infra_cnt_score = Column(Float)
    register_date = Column(DateTime)
    update_date = Column(DateTime)


class LogClick(Base):
    __tablename__ = "LOG_CLICK"

    idx = Column(Integer, primary_key=True, index=True)
    ip_address = Column(VARCHAR(255))
    user_id = Column(Integer)
    item_id = Column(Integer)
    log_type = Column(CHAR(2))
    log_date = Column(DateTime)