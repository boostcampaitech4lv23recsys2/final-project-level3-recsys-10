# models/test_model.py

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class Test(Base):
    __tablename__ = "test_user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)