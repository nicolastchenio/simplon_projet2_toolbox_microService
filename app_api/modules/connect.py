"""
Database connection configuration using SQLAlchemy.

This module initializes the database engine and session used by the API.
The application uses a local SQLite database stored in app_api/data/.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Définir le chemin du fichier SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "testsqlite.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# URL de connexion SQLAlchemy pour SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Création de l'engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # requis pour SQLite et threads multiples
)

# Session locale pour les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour la définition des modèles
Base = declarative_base()


def get_db():
    """
    Dependency function to provide a database session.

    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()