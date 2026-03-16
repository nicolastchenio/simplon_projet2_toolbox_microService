# tutoriel projet2 orchestration #

ATTENTION : suite a des probleme de version avec python 3.13 j ai du passer en cours de developpement en python 3.11

## phase A ##
### Étape 1 — Vérifier la structure du projet ###
#### Créer la structure suivante dans app_api : ####
```
.
├── app_api
│   ├── main.py
│   ├── pyproject.toml
│   ├── maths
│   │   ├── __init__.py
│   │   └── mon_module.py
│   ├── modules
│   │   ├── __init__.py
│   │   ├── connect.py
│   │   └── crud.py
│   ├── models
│   │   ├── __init__.py
│   │   └── models.py
│   └── data
│       └── moncsv.csv
│
├── app_front
│   ├── main.py
│   ├── pages
│   │   ├── 0_insert.py
│   │   └── 1_read.py
│   ├── pyproject.toml
│   └── Dockerfile
│
├── tests
│   └── test_math_csv.py
```
et j ai supprimé "test_main.py" du dossier "tests"

### Étape 2 — Implémenter la base SQLite avec SQLAlchemy ###

1) Créer la connexion dans app_api/modules/connect.py.

Responsabilités :
- créer l’engine SQLAlchemy
- créer la session
- créer la base SQLite locale
- 
```
"""
Database connection configuration using SQLAlchemy.

This module initializes the database engine and session used by the API.
During development, the application uses a local SQLite database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency used by FastAPI to provide a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
2) Créer le modèle SQLAlchemy
   
Dans app_api/models/models.py :

```
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
```

3) Implémenter les opérations CRUD

Dans app_api/modules/crud.py :

```
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
```

4) fichier pyproject.toml dans app_api

supprimer "pyproject.toml" ainsi que le dossier  ".venv" a la racine de mon projet  

creer le fichier "pyproject.toml"  dans le dossier "app_api"

deacitivate mo ancien environnement "venv"
et activer le nouveau environnement 
```
.venv\Scripts\activate
```


```
cd app_api
uv init
uv add fastapi
uv add uvicorn
uv add sqlalchemy
uv add pydantic
uv add pytest --dev
uv add pytest-cov --dev
```
```
uv sync
```

Ajouter la config pytest demandée par le projet dans app_api/pyproject.toml
```
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests"]
```

Vérifier que tout fonctionne
```
uv run python -c "import fastapi, sqlalchemy"
```

5) brancher l’API FastAPI avec la base de données et le CRUD

dans app_api/main.py :

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

"""
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
"""

6) Test
   
A la racine du projet:

"""
uv run uvicorn app_api.main:app --reload
"""
Ouvrir dans le navigateur :
http://127.0.0.1:8000/docs

Tester l’insertion et la lecture des données avec les endpoints /data :
"""
curl -X POST "http://127.0.0.1:8000/data?value_a=10&value_b=5&result=15"
"""
"""
curl "http://127.0.0.1:8000/data"
"""

Vérifier la base SQLite (facultatif) :
"""
sqlite3 app_api/test.db "SELECT * FROM data;"
"""