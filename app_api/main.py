"""
FastAPI application entry point.

Provides API endpoints to insert and list mathematical operations.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app_api.modules.connect import Base, engine, get_db
from app_api.modules.crud import create_data, get_all_data
from .models.models import Operation

# Crée les tables SQLite si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Operations API", description="API for managing operations in SQLite database", version="1.0.0")

@app.get("/")
def read_root():
    """
    Root endpoint.

    Returns a simple message to indicate that the API is running.

    Returns:
        dict: A dictionary with a message.
    """
    return {"message": "API is running"}


@app.post("/operations/")
def add_operation(operation: str, a: float, b: float | None = None, db: Session = Depends(get_db)):
    """
    Add a new mathematical operation.

    Args:
        operation (str): Operation type ("add", "sub", "square")
        a (float): First operand
        b (float | None): Second operand (optional)
        db (Session): Database session (dependency)

    Returns:
        dict: Created operation info
    """
    return create_data(db, operation, a, b).__dict__

@app.get("/operations/")
def list_operations(db: Session = Depends(get_db)):
    """
    List all operations stored in the database.

    Args:
        db (Session): Database session (dependency)

    Returns:
        list[dict]: List of operations as dictionaries
    """
    operations = get_all_data(db)
    return [op.__dict__ for op in operations]