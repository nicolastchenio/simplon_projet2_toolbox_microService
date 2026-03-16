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
