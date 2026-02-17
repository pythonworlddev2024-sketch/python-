"""
Gestion de la base de données utilisateurs
"""
import json
import hashlib
from pathlib import Path
from config import USERS_DB_FILE


def hash_password(password: str) -> str:
    """Hacher un mot de passe avec SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    """Charger la base de données utilisateurs"""
    if USERS_DB_FILE.exists():
        with open(USERS_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(users: dict):
    """Sauvegarder la base de données utilisateurs"""
    with open(USERS_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def user_exists(email: str) -> bool:
    """Vérifier si un utilisateur existe"""
    users = load_users()
    return email.lower() in users


def create_user(email: str, password: str) -> bool:
    """Créer un nouvel utilisateur"""
    if user_exists(email):
        return False
    
    users = load_users()
    users[email.lower()] = {
        "email": email.lower(),
        "password": hash_password(password),
        "created_at": str(Path(__file__).parent.parent / "data" / email.lower())
    }
    save_users(users)
    return True


def verify_user(email: str, password: str) -> bool:
    """Vérifier les identifiants d'un utilisateur"""
    users = load_users()
    user = users.get(email.lower())
    
    if user is None:
        return False
    
    return user["password"] == hash_password(password)


def get_user_data_path(email: str) -> Path:
    """Obtenir le chemin du dossier de données de l'utilisateur"""
    from config import USERS_DIR
    user_path = USERS_DIR / email.lower()
    user_path.mkdir(parents=True, exist_ok=True)
    return user_path
