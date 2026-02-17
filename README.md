# DataViz AI Analytics - Application Web d'Analyse de Données

Une application web complète en Python (Streamlit) pour l'analyse, la visualisation et la prédiction de données avec IA gratuite.

## 🌟 Fonctionnalités

### 1. **Authentification**
- ✅ Système Login/Sign In
- ✅ Gestion des utilisateurs
- ✅ Un utilisateur = un seul compte
- ✅ Sauvegarde sécurisée des données (hachage SHA256)

### 2. **Importation de Données**
- ✅ Upload CSV et Excel
- ✅ Aperçu immédiat des données
- ✅ Assistant IA initial pour comprendre les données
- ✅ Chatbot intégré

### 3. **Nettoyage de Données**
- ✅ Analyse automatique (Max, Min, Moyenne, etc.)
- ✅ Détection des types (Quantitative/Qualitative)
- ✅ Visualisation des doublons
- ✅ Gestion des valeurs aberrantes (Boxplot)
- ✅ Remplissage des valeurs manquantes
- ✅ Compteur des modifications (Avant/Après)
- ✅ Export des données nettoyées (CSV/Excel)

### 4. **Visualisation Interactive**
- ✅ Sélection multi-variables
- ✅ Graphiques automatiques (Scatter, Line, Bar, Histogram, Box, Violin)
- ✅ Graphiques interactifs (Plotly)
- ✅ Commentaires AI sur les tendances

### 5. **Prédictions (Machine Learning)**
- ✅ Sélection automatique de features
- ✅ Sliders pour les variables numériques
- ✅ Dropdowns pour les variables catégorielles
- ✅ Validation du formulaire
- ✅ Affichage des prédictions
- ✅ Importance des variables

### 6. **Assistant IA Flottant**
- ✅ Chat latéral pour les questions
- ✅ Conseils d'analyse
- ✅ Réponses en fonction des données

## 📋 Structure du Projet

```
data_analysis_app/
├── app.py                    # Application principale
├── config.py                 # Configuration
├── pages/
│   ├── __init__.py
│   ├── auth.py              # Authentification
│   ├── home.py              # Accueil
│   ├── upload.py            # Importation
│   ├── cleaning.py          # Nettoyage
│   └── visualization.py     # Visualisation & Prédictions
├── utils/
│   ├── __init__.py
│   ├── database.py          # Gestion utilisateurs
│   ├── data_processor.py    # Traitement des données
│   ├── ml_model.py          # Modèles IA
│   └── ai_helper.py         # Assistant IA
└── data/
    ├── users/               # Données utilisateurs
    └── users.json           # Base de données utilisateurs
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.8+
- pip ou conda

### Étapes

1. **Clonez ou créez le projet**
```bash
cd /Users/fati/python/data_analysis_app
```

2. **Créez un environnement virtuel (si nécessaire)**
```bash
python -m venv .venv
source .venv/bin/activate  # Sur macOS/Linux
# ou
.venv\Scripts\activate     # Sur Windows
```

3. **Installez les dépendances**
```bash
pip install streamlit pandas plotly scikit-learn openpyxl requests langchain huggingface-hub
```

4. **Lancez l'application**
```bash
streamlit run app.py
```

5. **Ouvrez votre navigateur**
L'application s'ouvrira automatiquement à `http://localhost:8501`

## 📝 Utilisation

### Première visite
1. Cliquez sur "Inscription" et créez un compte
2. Connectez-vous avec vos identifiants
3. Cliquez sur "Commencer" pour accéder à l'application

### Workflow d'analyse
1. **Importation** → Uploadez un fichier CSV ou Excel
2. **Nettoyage** → Nettoyez automatiquement vos données
3. **Visualisation** → Explorez vos données avec des graphiques interactifs
4. **Prédiction** → Faites des prédictions avec le ML
5. **Export** → Téléchargez vos résultats

## 🤖 Configuration de l'IA Gratuite

### Option 1: Hugging Face (Recommandé)
```python
# Dans config.py
AI_PROVIDER = "huggingface"
HUGGINGFACE_MODEL = "mistral-7b"
```

### Option 2: Groq (Très rapide)
```bash
pip install groq
# Dans config.py
AI_PROVIDER = "groq"
```

### Option 3: g4f (Pas d'authentification)
```bash
pip install g4f
# Dans config.py
AI_PROVIDER = "g4f"
```

## 🎨 Personnalisation

Vous pouvez personnaliser les couleurs dans `config.py`:
```python
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2ecc71"
DANGER_COLOR = "#e74c3c"
WARNING_COLOR = "#f39c12"
```

## 📊 Formats Supportés

- **Import**: CSV, XLSX, XLS
- **Export**: CSV, Excel

## ⚠️ Limites

- Taille maximale des fichiers: 50 MB
- Nombre maximum de lignes: Dépend de la RAM disponible
- Support des modèles: Modèles gratuits uniquement

## 🔒 Sécurité

- Les mots de passe sont hachés avec SHA256
- Un utilisateur = un seul compte (pas de doublons)
- Les données sont stockées localement par utilisateur
- Pas d'envoi de données vers des serveurs externes (configurable)

## 📚 Bibliothèques Utilisées

- **Streamlit** - Framework web
- **Pandas** - Manipulation de données
- **Plotly** - Visualisations interactives
- **Scikit-learn** - Machine Learning
- **Langchain** - Intégration IA

## 🚧 Prochaines Étapes

- [ ] Intégration d'une IA avancée (GPT gratuit)
- [ ] Partage de datasets entre utilisateurs
- [ ] Stockage cloud
- [ ] API REST
- [ ] Dashboard temps réel
- [ ] Modèles pré-entraînés personnalisés

## 📧 Support

Pour des questions ou des suggestions, veuillez:
1. Consulter la section FAQ
2. Ouvrir une issue GitHub
3. Contacter le support

## 📄 Licence

Ce projet est open source sous la licence MIT.

## 👨‍💻 Auteur

Créé avec ❤️ pour simplifier l'analyse de données

---

**Bon analyse!** 📊✨
