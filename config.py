# Configuration globale de l'application
import os
from pathlib import Path

# Répertoires
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
USERS_DIR = DATA_DIR / "users"

# Créer les répertoires s'ils n'existent pas
USERS_DIR.mkdir(parents=True, exist_ok=True)

# Base de données utilisateurs (fichier JSON pour simplicité)
USERS_DB_FILE = DATA_DIR / "users.json"

# Configuration Streamlit
APP_TITLE = "DataViz AI Analytics"
APP_ICON = "📊"

# Couleurs et thème
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2ecc71"
DANGER_COLOR = "#e74c3c"
WARNING_COLOR = "#f39c12"

# Configuration des fichiers uploadés
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# Configuration pour les modèles IA gratuits
# Option 1: Hugging Face (nécessite une clé API gratuite)
# Option 2: Groq (gratuit avec limite de requests)
# Option 3: g4f (GUI for Free)
AI_PROVIDER = "huggingface"  # ou "groq" ou "g4f"
HUGGINGFACE_MODEL = "mistral-7b"  # Modèle gratuit
