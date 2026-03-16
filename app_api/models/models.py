"""
ORM models for the application.

Defines the Operation table to store mathematical operations.
"""

from sqlalchemy import Column, Integer, String, Float
from ..modules.connect import Base  # importer Base depuis connect, pas depuis lui-même

class Operation(Base):
    """
    SQLAlchemy ORM model for a mathematical operation.

    Attributes:
        id (int): Primary key.
        operation (str): Operation type ("add", "sub", "square").
        a (float): First operand.
        b (float | None): Second operand (optional for square).
    """
    __tablename__ = "operations"
    __table_args__ = {"extend_existing": True}  # Evite l'erreur "table already defined"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, nullable=False)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=True)