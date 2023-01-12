# models/test_model.py

from sqlalchemy import Column, String, CHAR
from sqlalchemy.orm import relationship
from db.session import Base

class HobbangTest(Base):
    __tablename__ = "INFRA"

    infra_type = Column(CHAR, primary_key=True, index=True)
    infra = Column(String)