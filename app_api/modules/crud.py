"""
CRUD operations for the Operation model.

Provides functions to insert and retrieve operations from the database.
"""

from sqlalchemy.orm import Session
from app_api.models.models import Operation

def create_data(db: Session, operation: str, a: float, b: float | None = None) -> Operation:
    """
    Insert a new operation into the database.

    Args:
        db (Session): Database session
        operation (str): Operation type ("add", "sub", "square")
        a (float): First operand
        b (float | None): Second operand (optional)

    Returns:
        Operation: The newly created Operation object
    """
    db_operation = Operation(operation=operation, a=a, b=b)
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation

def get_all_data(db: Session) -> list[Operation]:
    """
    Retrieve all operations from the database.

    Args:
        db (Session): Database session

    Returns:
        list[Operation]: List of Operation objects
    """
    return db.query(Operation).all()