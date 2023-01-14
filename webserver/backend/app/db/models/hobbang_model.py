# models/test_model.py

from sqlalchemy import Column, String, CHAR
from sqlalchemy.orm import relationship
from db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, DateTime, Float

class HobbangTest(Base):
    __tablename__ = "INFRA"

    infra_type = Column(CHAR, primary_key=True, index=True)
    infra = Column(String)
    
    
class User(Base): 
    __tablename__ = "USERS_INFO"

    user_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    pw = Column(VARCHAR(255), nullable=False)
    user_gu = Column(VARCHAR(255), nullable=False)
    user_age = Column(Integer, nullable=False)
    user_sex = Column(Integer, nullable=False)
    user_type =  Column(CHAR(1), nullable=False)

    # user = relationship("User", backref="userinfo")
