# Simplon Projet 2 – Toolbox Microservice

![CI Status](https://github.com/nicolastchenio/simplon_projet2_toolbox_microService/actions/workflows/ci.yml/badge.svg)
![Coverage](https://raw.githubusercontent.com/nnicolastchenio/simplon_projet2_toolbox_microService/main/coverage.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Lint](https://img.shields.io/badge/lint-ruff-purple)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

**Python Toolbox Microservice** est une évolution du projet initial vers une architecture modulaire et distribuée. Ce projet démontre la mise en place d'une architecture micro-services complète, sécurisée et orchestrée :

- **Architecture Monorepo** gérée avec `uv`.
- **Backend API** performant avec FastAPI.
- **Frontend Interactif** avec Streamlit.
- **Persistance des données** (PostgreSQL / SQLite).
- **Tests unitaires et d'intégration** avec Pytest.
- **Qualité de code** via Ruff.
- **CI/CD & Sécurité** : Scan de secrets (Gitleaks) et déploiement automatisé.

---

## Project Structure

```plaintext
.
├── .github/                    
│   ├── workflows/
│   │   ├── ci.yml             # Linting, Tests, Gitleaks
│   │   └── docs.yml           # Documentation Sphinx
│   └── CODE_OF_CONDUCT.md
│   └── CONTRIBUTING.md          
├── app_api/                   # Service Backend (FastAPI)
│   ├── maths/                 # Logique métier mathématique
│   ├── models/                # Modèles de données (Pydantic/SQLAlchemy)
│   ├── modules/               # Connexion et CRUD
│   ├── data/                  # Données statiques (CSV)
│   └── main.py                # Point d'entrée de l'API
├── app_front/                 # Service Frontend (Streamlit)
│   ├── pages/                 # Pages de saisie et d'affichage
│   └── main.py                # Point d'entrée du Front
├── tests/                     # Tests globaux (API et Logique)
│   ├── test_api.py
│   └── test_math_csv.py   
├── docs/                      # Documentation technique (Sphinx)
├── .dockerignore 
├── .gitignore 
├── pyproject.toml             # Configuration du Monorepo (uv workspace)
├── uv.lock                    
├── README.md
└── LICENSE
```

---

## Installation

Ce projet utilise **uv** pour la gestion des dépendances et de l'espace de travail (workspace).

### 1. Prérequis
Assurez-vous d'avoir `uv` installé :
```bash
pip install uv
```

### 2. Cloner le dépôt
```bash
git clone https://github.com/nicolastchenio/simplon_projet2_toolbox-microservice.git
cd simplon_projet2_toolbox-microservice
```

### 3. Synchroniser l'environnement
Depuis la racine du projet :
```bash
uv sync
```
Cette commande installe les dépendances pour tous les membres de l'espace de travail (`app_api` et `app_front`).

---

## Running the Application (Local)

Le projet nécessite le lancement de deux services distincts dans deux terminaux différents depuis la racine du projet.

### 1. Terminal 1 : Backend API (FastAPI)
```bash
# Lancer l'API avec rechargement automatique (Hot Reload)
uv run uvicorn app_api.main:app --reload
```
- **API** : [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Documentation interactive (Swagger)** : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Terminal 2 : Frontend (Streamlit)
```bash
# Se déplacer dans le dossier front et lancer l'interface
cd app_front
uv run streamlit run main.py
```
- **Interface Utilisateur** : [http://localhost:8501](http://localhost:8501)

---

## Running Tests

Exécutez la suite complète de tests depuis la racine :
```bash
uv run pytest
```

Pour générer un rapport de couverture :
```bash
uv run pytest --cov=app_api --cov-report=term-missing
```

---

## Code Quality

Nous utilisons **Ruff** pour le linting et la mise en conformité du code :

```bash
uv run ruff check .
```

---

## Continuous Integration & Security

Le projet intègre une pipeline CI/CD robuste :

- **Tests & Linting** : Lancés à chaque commit.
- **Sécurité (Gitleaks)** : Vérification automatique de l'absence de secrets ou clés API dans l'historique Git.
- **Documentation** : Génération automatique de la documentation Sphinx.

---

## Contributing

Les contributions sont les bienvenues. Veuillez consulter **CONTRIBUTING.md** pour plus de détails.

---

## Contributors

Projet développé par :
- nicolas tchenio

---

## License

Ce projet est sous licence **MIT**. Voir le fichier **LICENSE** pour plus de détails.
