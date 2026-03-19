"""Database connection configuration using SQLAlchemy.

This module initializes the database engine and session used by the API.
The application uses a local SQLite database stored in app_api/data/.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Charger les variables d'environnement
load_dotenv()

# URL de connexion PostgreSQL (host 'db' pour Docker Compose)
DATABASE_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@db:{os.getenv('POSTGRES_PORT', 5432)}/"
    f"{os.getenv('POSTGRES_DB')}"
)

# Création de l'engine
engine = create_engine(DATABASE_URL)

# Session locale pour les transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour la définition des modèles
Base = declarative_base()


def get_db():
    """Dependency function to provide a database session.

    Yields:
        Session: SQLAlchemy session

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
