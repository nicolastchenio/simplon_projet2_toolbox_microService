"""
Database models used by the application.
"""

from sqlalchemy import Column, Integer, Float
from app_api.modules.connect import Base


class Data(Base):
    """
    SQLAlchemy model representing stored numeric data.
    """

    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    value_a = Column(Float)
    value_b = Column(Float)
    result = Column(Float)