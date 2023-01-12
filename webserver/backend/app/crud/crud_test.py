# crud/crud_test.py

from sqlalchemy.orm import Session
from db.models.test_model import Test

def get_items(db: Session):
    return db.query(Test).all()