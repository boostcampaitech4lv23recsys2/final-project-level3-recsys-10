# crud/hobbang_crud_test.py

from sqlalchemy.orm import Session
from db.models.hobbang_model import HobbangTest
from pydantic import BaseModel, Field
from db.models import hobbang_model

def get_infra(db: Session):
    return db.query(HobbangTest).all()

class UserCreate(BaseModel):
    """
    despription: 새로운 유저 추가
    application: 회원가입
    """
    # user_id: int = Field(None) # UUID = Field(default_factory=uuid4)
    name: str = Field(None)
    pw: str = Field(None)
    user_gu: str = Field(None)
    user_sex: int = Field(None)
    user_age: int = Field(None)
    user_type: str = Field(None)


def create_user(db: Session, user: UserCreate):
    # max_id_before = db.query(func.max(models.User.user_id)).scalar()
    db_user = hobbang_model.User(
                    name = user.name,
                    pw=user.pw, 
                    user_gu=user.user_gu,
                    user_sex=user.user_sex,
                    user_age=user.user_age,
                    user_type=user.user_type,
                     )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user