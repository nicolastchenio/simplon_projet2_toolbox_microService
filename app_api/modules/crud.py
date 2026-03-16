"""
CRUD operations for the database.
"""

from sqlalchemy.orm import Session
from app_api.models.models import Data


def create_data(db: Session, value_a: float, value_b: float, result: float):
    """
    Insert new data into the database.
    """

    data = Data(value_a=value_a, value_b=value_b, result=result)

    db.add(data)
    db.commit()
    db.refresh(data)

    return data


def get_all_data(db: Session):
    """
    Retrieve all stored data from the database.
    """

    return db.query(Data).all()