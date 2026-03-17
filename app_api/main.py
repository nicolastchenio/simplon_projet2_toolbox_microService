"""
FastAPI application entry point.

Provides API endpoints to insert, update, delete, and list mathematical operations.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app_api.modules.connect import Base, engine, get_db
from app_api.modules.crud import (
    create_data, get_all_data, update_operation, delete_operation
)

# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


def serialize_operation(op):
    """
    Convert SQLAlchemy object to JSON serializable dict.
    """
    return {
        "id": op.id,
        "operation": op.operation,
        "a": op.a,
        "b": op.b,
        "result": op.result
    }


@app.get("/")
def read_root():
    return {"message": "API is running"}


@app.post("/operations/")
def add_operation(operation: str, a: float, b: float | None = None, db: Session = Depends(get_db)):
    try:
        op = create_data(db, operation, a, b)
        return serialize_operation(op)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/operations/")
def list_operations(db: Session = Depends(get_db)):
    operations = get_all_data(db)
    return [serialize_operation(op) for op in operations]


@app.put("/operations/{operation_id}")
def update_operation_endpoint(operation_id: int, operation: str, a: float, b: float | None = None, db: Session = Depends(get_db)):
    try:
        op = update_operation(db, operation_id, operation, a, b)
        return serialize_operation(op)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/operations/{operation_id}")
def delete_operation_endpoint(operation_id: int, db: Session = Depends(get_db)):
    success = delete_operation(db, operation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Operation not found")
    return {"message": "Operation deleted"}