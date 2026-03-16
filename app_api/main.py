"""
Main FastAPI application.

This module defines the API endpoints used to interact with the
database and the mathematical toolbox functions.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app_api.modules.connect import engine, Base, get_db
from app_api.modules.crud import create_data, get_all_data

app = FastAPI()

# création automatique des tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {"message": "API is running"}


@app.post("/data")
def add_data(value_a: float, value_b: float, result: float, db: Session = Depends(get_db)):
    """
    Insert a new record into the database.
    """
    return create_data(db, value_a, value_b, result)


@app.get("/data")
def read_data(db: Session = Depends(get_db)):
    """
    Retrieve all stored records.
    """
    return get_all_data(db)