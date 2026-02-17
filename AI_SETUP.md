# 🤖 Guide d'Activation de l'IA

L'assistant IA de DataViz AI Analytics fonctionne de deux manières :

## 1️⃣ Sans Configuration (Recommandé pour commencer)
L'assistant utilise des réponses intelligentes basées sur l'analyse des données.
✅ **Fonctionne immédiatement**
✅ **Gratuit**
✅ **Pas de configuration nécessaire**

## 2️⃣ Avec Groq (IA Avancée - Gratuit)
Pour des réponses plus intelligentes et contextuelles :

### Étape 1 : Créer un compte Groq
1. Allez sur [console.groq.com](https://console.groq.com)
2. Créez un compte gratuit
3. Confirmez votre email

### Étape 2 : Générer une clé API
1. Allez sur [console.groq.com/keys](https://console.groq.com/keys)
2. Cliquez sur "Create New API Key"
3. Copiez votre clé API

### Étape 3 : Configurer l'app (2 options)

#### Option A : Variable d'environnement (Recommandée)
```bash
# Dans un terminal
export GROQ_API_KEY="gsk_votre_clé_api_ici"

# Puis relancez l'app
cd /Users/fati/python/data_analysis_app
streamlit run app.py
```

#### Option B : Fichier .env
1. Renommez `.env.example` en `.env`
2. Remplacez `gsk_votre_clé_ici` par votre vraie clé
3. Relancez l'app

### Étape 4 : Testez !
1. Uploadez un fichier CSV
2. Posez une question dans le chatbot
3. L'IA répondra avec des insights avancés ! 🚀

## 🆓 Groq - Pourquoi c'est gratuit ?
- **Modèle open-source** : Mixtral 8x7B (très puissant)
- **API gratuite** : Pas besoin de carte de crédit
- **Rapide** : 230 tokens/s (beaucoup plus rapide que GPT-3.5)
- **Pas de limites** : Utilisez-le autant que vous voulez

## ⚠️ Limites
- Groq a des limites douces sur les requêtes (générougement pour l'usage personnel)
- Idéal pour l'analyse de données et les questions techniques

## 🆘 Problèmes ?
1. Vérifiez votre clé API (pas d'espaces)
2. Assurez-vous que `groq` est installé :
   ```bash
   pip install groq
   ```
3. Relancez l'app après configuration
4. Sans clé API, l'assistant fonctionne quand même ! 😊

## 🎓 Exemples de questions pour l'IA
- "Combien de valeurs manquantes dans mes données ?"
- "Quelles colonnes dois-je nettoyer en priorité ?"
- "Y a-t-il des anomalies dans ces données ?"
- "Comment améliorer la qualité de mon dataset ?"
- "Quels modèles ML recommandez-vous ?"

---

**Enjoy! 🚀**
