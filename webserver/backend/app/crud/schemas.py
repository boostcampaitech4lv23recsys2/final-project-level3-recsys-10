from typing import List, Union, Optional, Dict, Any
from sqlalchemy import CHAR
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class UserBase(BaseModel):
    """
    description: 유저 한 명에 대한 정보
    """
    user_id: int = Field(None) 
    name: str = Field(None)

class UserCreate(UserBase):
    """
    despription: 새로운 유저 추가
    application: 회원가입
    """
    # user_id: int = Field(None) # UUID = Field(default_factory=uuid4)
    pw: str = Field(None)
    user_gu: str = Field(None)
    user_age: int = Field(None)
    user_sex: int = Field(None)
    user_type: str = Field(None)

class User(UserBase):
    """
    description: 유저 한 명에 대한 정보 (조회용)
    """
    password: str = Field(None)
    gender: str = Field(None)
    birth: datetime = Field(default_factory=datetime.now)
    class Config:
        orm_mode = True


class InferenceResult(BaseModel):
    house_scores: Dict = Field(None)

class MapZoom(InferenceResult):
    min_lat: float = Field(None)
    min_lng: float = Field(None)
    max_lat: float = Field(None)
    max_lng: float = Field(None)