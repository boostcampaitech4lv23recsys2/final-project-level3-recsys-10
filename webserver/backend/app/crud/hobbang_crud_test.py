# crud/hobbang_crud_test.py

from sqlalchemy.orm import Session
from db.models.hobbang_model import HobbangTest

def get_infra(db: Session):
    return db.query(HobbangTest).all()