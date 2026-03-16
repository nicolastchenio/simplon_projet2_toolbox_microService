# La version de python
FROM python:3.11-slim
# On récupère uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# on crée un dossier pour l'application
WORKDIR /app
# On copie uniquement les fichiers de dépendances
COPY pyproject.toml uv.lock ./
# On installe les paquets (uv sync -> .venv)
RUN uv pip install --system -r pyproject.toml
# On copie le reste
COPY . .
# On exécute le code (ici "-m"permet aux imports relatifs de fonctionner correctement si tu conserves le . => voir app/main.py avec "from .modules.mon_module import add, print_data, square, sub" ou "/modules" est un chemin relatif)
CMD ["python", "-m", "app.main"]
# pour chemin absolu si dans app/main.py j avais mis "from modules.mon_module import add, print_data, square, sub"
# CMD ["python", "app/main.py"]