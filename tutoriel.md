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
│   ├── test_api.py
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
```
2) Créer le modèle SQLAlchemy
   
Dans app_api/models/models.py :

```
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
```

3) Implémenter les opérations CRUD

Dans app_api/modules/crud.py :

```
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

```
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
```

# création automatique des tables
Base.metadata.create_all(bind=engine)

```
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
```

6) Test
   
A la racine du projet:

```
uv run uvicorn app_api.main:app --reload
```
Ouvrir dans le navigateur :
http://127.0.0.1:8000/docs

Tester l’insertion et la lecture des données avec les endpoints /data :
```
curl -X POST "http://127.0.0.1:8000/operations/?operation=add&a=10&b=5"
```
```
curl "http://127.0.0.1:8000/data"
```

Vérifier la base SQLite (facultatif) :
```
sqlite3 app_api/test.db "SELECT * FROM data;"
```

### Étape 3 — Implémenter Streamlit ###

1) fichier pyproject.toml dans app_api
```
cd app_front
uv init
uv add streamlit
uv add sqlalchemy requests pandas
```

activer le nouveau environnement 
```
.venv\Scripts\activate
```

Après installation, tu peux vérifier que Streamlit est disponible :

```
uv run streamlit --version
```

Ensuite, pour lancer ton frontend Streamlit :
```
uv run streamlit run main.py
```

2) app_front/main.py

```
"""
Streamlit application entry point.

This module initializes the main interface of the frontend application.
It provides a simple landing page explaining the purpose of the app.

The frontend communicates with the FastAPI backend to:
- Insert new mathematical operations
- Retrieve stored operations from the database
"""

import streamlit as st

st.set_page_config(
    page_title="Math Operations App",
    page_icon="🧮",
    layout="centered",
)

st.title("Math Operations Application")

st.write(
    """
This Streamlit application allows users to interact with a backend API
that stores mathematical operations in a database.

Available features:
- Insert new mathematical operations
- View previously stored operations
"""
)

st.info(
    "Use the navigation menu on the left to insert or view operations."
)

```

3) app_front/pages/0_insert.py

```
"""
Streamlit page used to insert mathematical operations.

This page provides a form allowing the user to create a new
mathematical operation. The operation is sent to the FastAPI backend
via an HTTP POST request.

Supported operations:
- add
- sub
- square

The backend API stores the operation in a SQLite database.
"""

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/operations/"

st.title("Insert a Mathematical Operation")

operation = st.selectbox(
    "Select operation",
    ["add", "sub", "square"]
)

a = st.number_input("Value A", value=0.0)

b = None
if operation != "square":
    b = st.number_input("Value B", value=0.0)

if st.button("Submit operation"):
    params = {
        "operation": operation,
        "a": a,
        "b": b,
    }

    try:
        response = requests.post(API_URL, params=params)

        if response.status_code == 200:
            st.success("Operation successfully stored.")
            st.json(response.json())
        else:
            st.error("Error while inserting operation.")

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the API. Make sure FastAPI is running.")
```

4) app_front/pages/1_read.py

```
"""
Streamlit page used to display stored operations.

This page retrieves all mathematical operations stored in the
database by calling the FastAPI backend API.

The retrieved data is displayed in a tabular format using
a pandas DataFrame.
"""

import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/operations/"

st.title("Stored Mathematical Operations")

if st.button("Load operations"):
    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            data = response.json()

            if len(data) == 0:
                st.warning("No operations found in the database.")
            else:
                df = pd.DataFrame(data)
                st.dataframe(df)

        else:
            st.error("Error while retrieving operations.")

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the API. Make sure FastAPI is running.")


```
5) pour tester
- Terminal 1 — API
Depuis la racine du projet :
```
cd app_api
.venv\Scripts\activate
cd..

uv run uvicorn app_api.main:app --reload
```

API disponible sur :

http://127.0.0.1:8000

- Terminal 2 — Frontend
```
cd app_front
.venv\Scripts\activate
uv run streamlit run main.py
```

Interface :

http://localhost:8501

- modification de fichier pour interger resultat
=> suppression de testSquilte.db 
=> recrer le fichier testSquilte.db:

```
cd app_api
uv add pandas
uv sync
.venv\Scripts\activate   # activer ton environnement
uv run uvicorn main:app --reload
```

```
curl -X POST "http://127.0.0.1:8000/operations/?operation=add&a=10&b=5" -H "accept: application/json"
curl -X POST "http://127.0.0.1:8000/operations/?operation=square&a=7" -H "accept: application/json"
curl -X GET "http://127.0.0.1:8000/operations/" -H "accept: application/json"
curl -X PUT "http://127.0.0.1:8000/operations/1?operation=sub&a=20&b=3" -H "accept: application/json"
curl -X DELETE "http://127.0.0.1:8000/operations/1" -H "accept: application/json"
```

### Étape 4 — Validez votre API avec Pytest (maths et api) ###

- creation du fichier test_api.py
- suppression de test_main.py
- modification de test_math_csv.py

pour lancer les tests :
```
uv run pytest
```
ou 

```
uv run --project app_api pytest --cov=app_api tests/
```