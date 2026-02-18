"""
Assistant IA pour l'analyse de données
Utilise analyse locale intelligente + Google Gemini (gratuit) optionnel + Hugging Face API fallback
"""
import os
import re
import pandas as pd
import numpy as np
import requests
from difflib import SequenceMatcher


def fuzzy_contains(text, keywords, threshold=0.75):
    """Cherche si un mot similaire à keywords existe dans text (tolère les fautes)"""
    words = text.lower().split()
    for keyword in keywords:
        for word in words:
            similarity = SequenceMatcher(None, keyword.lower(), word).ratio()
            if similarity >= threshold:
                return True
    return False


class UnrecognizedQuestion(Exception):
    """Exception levée quand DataAnalyzerAI ne reconnaît pas la question"""
    pass


class DataAnalyzerAI:
    """IA conversationnelle pour analyser les données et répondre à TOUT"""
    
    def __init__(self, df):
        self.df = df
        self.analysis_cache = {}
        self._analyze_data()
    
    def _analyze_data(self):
        """Analyse complète du DataFrame"""
        self.analysis_cache = {
            'shape': (len(self.df), len(self.df.columns)),
            'columns': self.df.columns.tolist(),
            'dtypes': {col: str(self.df[col].dtype) for col in self.df.columns},
            'missing': self.df.isnull().sum().to_dict(),
            'duplicates': len(self.df[self.df.duplicated()]),
            'numeric_cols': self.df.select_dtypes(include=[np.number]).columns.tolist(),
            'categorical_cols': self.df.select_dtypes(include=['object']).columns.tolist(),
            'stats': {}
        }
        
        # Statistiques pour colonnes numériques
        for col in self.analysis_cache['numeric_cols']:
            self.analysis_cache['stats'][col] = {
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'std': float(self.df[col].std()),
                'q25': float(self.df[col].quantile(0.25)),
                'q75': float(self.df[col].quantile(0.75)),
                'trend': self._calculate_trend(self.df[col])
            }
    
    def _calculate_trend(self, series):
        """Calcule la tendance (augmente/diminue/stable)"""
        if len(series) < 2:
            return "stable"
        first_half = series.iloc[:len(series)//2].mean()
        second_half = series.iloc[len(series)//2:].mean()
        if second_half > first_half * 1.05:
            return "augmente"
        elif second_half < first_half * 0.95:
            return "diminue"
        return "stable"
    
    def answer_question(self, question: str) -> str:
        """Répond UNIQUEMENT à la question posée, sans suggestions supplémentaires"""
        q_lower = question.lower().strip()
        
        # === SALUTATIONS ===
        greetings = ['salut', 'hello', 'hi', 'bonjour', 'bonsoir', 'ça va', 'how are you', 'quoi de neuf']
        if fuzzy_contains(q_lower, greetings, threshold=0.65):
            return f"👋 Salut ! Vous avez {self.analysis_cache['shape'][0]} lignes et {self.analysis_cache['shape'][1]} colonnes."
        
        # === REMERCIEMENTS ===
        thanks = ['merci', 'thank you', 'thanks', 'gracias']
        if fuzzy_contains(q_lower, thanks, threshold=0.65):
            return "🙏 De rien !"
        
        # === PRÉDICTIONS/TENDANCES (EN PRIORITÉ) ===
        if fuzzy_contains(q_lower, ['prédict', 'prediction', 'predir', 'predit', 'predict', 'forecast', 'futur', 'future', 'tendance', 'trend', 'extrapoler'], threshold=0.65):
            # Si la question contient des paramètres (=, nombres), c'est une prédiction avancée → Gemini
            if '=' in q_lower or any(char.isdigit() for char in q_lower):
                raise UnrecognizedQuestion(question)
            
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Pas de colonnes numériques pour prédictions"
            
            # Chercher colonne spécifique
            for col in numeric_cols:
                if col.lower() in q_lower:
                    trend = self.analysis_cache['stats'][col]['trend']
                    if trend == "augmente":
                        return f"📈 {col}: En augmentation (continue à monter)"
                    elif trend == "diminue":
                        return f"📉 {col}: En diminution (continue à descendre)"
                    else:
                        return f"➡️ {col}: Stable (pas de changement majeur)"
            
            # Sinon toutes les colonnes
            trends = []
            for col in numeric_cols[:3]:
                trend = self.analysis_cache['stats'][col]['trend']
                emoji = "📈" if trend == "augmente" else "📉" if trend == "diminue" else "➡️"
                trends.append(f"{emoji} {col}: {trend}")
            return "🔮 Tendances:\n" + "\n".join(trends)
        
        # === LIGNES ===
        if fuzzy_contains(q_lower, ['ligne', 'row', 'enregistrement', 'observation', 'record'], threshold=0.65):
            if fuzzy_contains(q_lower, ['combien', 'nombre', 'how', 'total', 'quoi'], threshold=0.65):
                return f"📊 {self.analysis_cache['shape'][0]} lignes"
        
        # === COLONNES ===
        if fuzzy_contains(q_lower, ['colonne', 'column', 'variable', 'feature', 'champ'], threshold=0.65):
            if fuzzy_contains(q_lower, ['combien', 'nombre', 'how', 'quoi'], threshold=0.65):
                numeric = len(self.analysis_cache['numeric_cols'])
                categorical = len(self.analysis_cache['categorical_cols'])
                return f"📋 {self.analysis_cache['shape'][1]} colonnes ({numeric} numériques, {categorical} catégoriques)"
        
        # === DONNÉES MANQUANTES ===
        if fuzzy_contains(q_lower, ['manquant', 'missing', 'null', 'nan', 'vide', 'empty'], threshold=0.65):
            total_missing = sum(self.analysis_cache['missing'].values())
            if total_missing == 0:
                return "✅ 0 valeurs manquantes"
            else:
                top_missing = sorted(self.analysis_cache['missing'].items(), key=lambda x: x[1], reverse=True)[0]
                return f"⚠️ {total_missing} valeurs manquantes (colonne la plus touchée: {top_missing[0]} avec {top_missing[1]})"
        
        # === DOUBLONS ===
        if fuzzy_contains(q_lower, ['doublon', 'duplicate', 'doublons', 'duplique', 'répété', 'unique', 'identique'], threshold=0.65):
            dups = self.analysis_cache['duplicates']
            if dups == 0:
                return "✅ 0 doublons"
            else:
                return f"⚠️ {dups} doublons détectés"
        
        # === MOYENNE - EXTRAIRE LA COLONNE SI MENTIONNÉE ===
        if fuzzy_contains(q_lower, ['moyenne', 'mean', 'moyen', 'average', 'avg', 'moyene', 'moyennes', 'moy'], threshold=0.65):
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Aucune colonne numérique"
            
            # Chercher si colonne spécifique mentionnée
            for col in numeric_cols:
                if col.lower() in q_lower:
                    mean = self.analysis_cache['stats'][col]['mean']
                    return f"📊 Moyenne de {col}: {mean:.2f}"
            
            # Sinon retourner toutes
            stats = []
            for col in numeric_cols:
                mean = self.analysis_cache['stats'][col]['mean']
                stats.append(f"{col}: {mean:.2f}")
            return "📊 Moyennes:\n" + "\n".join(stats)
        
        # === MINIMUM ===
        if fuzzy_contains(q_lower, ['minimum', 'min'], threshold=0.65) and not fuzzy_contains(q_lower, ['max'], threshold=0.65):
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Aucune colonne numérique"
            
            # Chercher colonne spécifique
            for col in numeric_cols:
                if col.lower() in q_lower:
                    min_val = self.analysis_cache['stats'][col]['min']
                    return f"📊 Min de {col}: {min_val:.2f}"
            
            stats = []
            for col in numeric_cols:
                min_val = self.analysis_cache['stats'][col]['min']
                stats.append(f"{col}: {min_val:.2f}")
            return "📊 Minimales:\n" + "\n".join(stats)
        
        # === MAXIMUM ===
        if fuzzy_contains(q_lower, ['max', 'maximum'], threshold=0.65) and not fuzzy_contains(q_lower, ['min', 'minimum'], threshold=0.65):
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Aucune colonne numérique"
            
            # Chercher colonne spécifique
            for col in numeric_cols:
                if col.lower() in q_lower:
                    max_val = self.analysis_cache['stats'][col]['max']
                    return f"📊 Max de {col}: {max_val:.2f}"
            
            stats = []
            for col in numeric_cols:
                max_val = self.analysis_cache['stats'][col]['max']
                stats.append(f"{col}: {max_val:.2f}")
            return "📊 Maximales:\n" + "\n".join(stats)
        
        # === MIN ET MAX ENSEMBLE ===
        if fuzzy_contains(q_lower, ['min', 'minimum'], threshold=0.65) and fuzzy_contains(q_lower, ['max', 'maximum'], threshold=0.65):
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Aucune colonne numérique"
            
            # Chercher colonne spécifique
            for col in numeric_cols:
                if col.lower() in q_lower:
                    min_val = self.analysis_cache['stats'][col]['min']
                    max_val = self.analysis_cache['stats'][col]['max']
                    return f"📊 {col}: Min={min_val:.2f}, Max={max_val:.2f}"
            
            stats = []
            for col in numeric_cols:
                min_val = self.analysis_cache['stats'][col]['min']
                max_val = self.analysis_cache['stats'][col]['max']
                stats.append(f"{col}: Min={min_val:.2f}, Max={max_val:.2f}")
            return "📊 Min/Max:\n" + "\n".join(stats)
        
        # === ÉCART-TYPE / STD ===
        if fuzzy_contains(q_lower, ['écart', 'std', 'standard', 'deviation', 'variabilite', 'variation', 'dispersion', 'ecart'], threshold=0.65):
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Aucune colonne numérique"
            
            # Chercher colonne spécifique
            for col in numeric_cols:
                if col.lower() in q_lower:
                    std = self.analysis_cache['stats'][col]['std']
                    return f"📊 Écart-type de {col}: {std:.2f}"
            
            stats = []
            for col in numeric_cols:
                std = self.analysis_cache['stats'][col]['std']
                stats.append(f"{col}: {std:.2f}")
            return "📊 Écarts-types:\n" + "\n".join(stats)
        
        # === MÉDIANE ===
        if fuzzy_contains(q_lower, ['médiane', 'median', 'mediane', 'centre'], threshold=0.65):
            numeric_cols = self.analysis_cache['numeric_cols']
            if not numeric_cols:
                return "❌ Aucune colonne numérique"
            
            for col in numeric_cols:
                if col.lower() in q_lower:
                    median = self.analysis_cache['stats'][col]['median']
                    return f"📊 Médiane de {col}: {median:.2f}"
            
            stats = []
            for col in numeric_cols:
                median = self.analysis_cache['stats'][col]['median']
                stats.append(f"{col}: {median:.2f}")
            return "📊 Médianes:\n" + "\n".join(stats)
        
        # === RÉSUMÉ ===
        if fuzzy_contains(q_lower, ['résumé', 'resume', 'summary', 'apercu', 'overview', 'total', 'recap'], threshold=0.65):
            numeric_count = len(self.analysis_cache['numeric_cols'])
            cat_count = len(self.analysis_cache['categorical_cols'])
            total_missing = sum(self.analysis_cache['missing'].values())
            return f"""📊 Résumé:
- {self.analysis_cache['shape'][0]} lignes × {self.analysis_cache['shape'][1]} colonnes
- {numeric_count} numériques, {cat_count} catégoriques
- {self.analysis_cache['duplicates']} doublons, {total_missing} manquantes"""
        
        
        # === NETTOYAGE ===
        if fuzzy_contains(q_lower, ['nettoyer', 'clean', 'probleme', 'problème', 'issue', 'nettoie'], threshold=0.65):
            recs = []
            if self.analysis_cache['duplicates'] > 0:
                recs.append(f"Supprimer {self.analysis_cache['duplicates']} doublons")
            if sum(self.analysis_cache['missing'].values()) > 0:
                recs.append(f"Traiter {sum(self.analysis_cache['missing'].values())} manquantes")
            
            if not recs:
                return "✅ Données très propres, aucun nettoyage nécessaire"
            return "🧹 À faire:\n" + "\n".join(recs)
        
        # === VISUALISATION ===
        if fuzzy_contains(q_lower, ['visuali', 'graphique', 'plot', 'chart', 'graph', 'image', 'affiche'], threshold=0.65):
            return "📈 Utilisez l'onglet Visualisation pour créer: scatter, line, bar, histogram, box, violin"
        
        # === FALLBACK : Lever exception pour essayer Gemini ===
        raise UnrecognizedQuestion(question)


def get_ai_response(question: str, context: str = None, df=None) -> str:
    """
    Google Gemini répond à TOUTES les questions avec analyse avancée
    Inclut: statistiques descriptives, corrélations, tendances, distributions
    """
    
    api_key = ""
    try:
        import streamlit as st
        # Try session state first (user-provided key)
        api_key = st.session_state.get("google_api_key", "")
        # If not in session, try secrets
        if not api_key:
            candidates = [
                "GOOGLE_API_KEY", "google_api_key", "googleApiKey",
                "google.api_key", "googleapikey", "api_key"
            ]
            for key in candidates:
                if key in st.secrets:
                    api_key = st.secrets[key]
                    break
            # Try nested dict
            if not api_key and "google" in st.secrets:
                google_sect = st.secrets["google"]
                if isinstance(google_sect, dict):
                    api_key = google_sect.get("api_key") or google_sect.get("GOOGLE_API_KEY") or ""
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY", "")

    api_key = (api_key or "").strip()
    
    if not api_key:
        # Fallback: utiliser Hugging Face API (GRATUIT, pas de clé nécessaire)
        hf_response = try_huggingface_api(question, df)
        if hf_response:
            return hf_response
        # Si Hugging Face échoue, retourner erreur
        return "❌ Service IA temporairement indisponible. Veuillez réessayer."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Préparer le contexte AVANCÉ des données
        context_text = ""
        if df is not None and len(df) > 0:
            context_text = _build_advanced_context(df)
        
        prompt = f"""Tu dois répondre EXTRÊMEMENT BRIÈVEMENT en une ou deux phrases maximum.
Pas d'explications, pas de détails, pas de conseils.
Juste la réponse directe à la question.

{context_text}

Question: {question}

Réponse ultra-courte (1-2 phrases MAX):"""
        
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            return "❌ Pas de réponse de Gemini"
            
    except Exception as e:
        print(f"❌ Erreur Google: {str(e)}")
        # Fallback à Hugging Face en cas d'erreur Google aussi
        hf_response = try_huggingface_api(question, df)
        if hf_response:
            return hf_response
        return f"❌ Service indisponible: {str(e)}"


def _build_advanced_context(df) -> str:
    """
    Construit un contexte enrichi avec corrélations, distributions, tendances
    """
    lines = []
    lines.append(f"CONTEXTE DONNÉES:")
    lines.append(f"- Nombre total de lignes: {len(df)}")
    lines.append(f"- Nombre de colonnes: {len(df.columns)}")
    
    # Séparer numérique et catégorique
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # === STATISTIQUES DESCRIPTIVES AVANCÉES ===
    if numeric_cols:
        lines.append(f"\nSTATISTIQUES DESCRIPTIVES ({len(numeric_cols)} colonnes numériques):")
        for col in numeric_cols:
            try:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    mean_val = col_data.mean()
                    std_val = col_data.std()
                    min_val = col_data.min()
                    max_val = col_data.max()
                    median_val = col_data.median()
                    q1 = col_data.quantile(0.25)
                    q3 = col_data.quantile(0.75)
                    
                    # Calculer la variabilité (coefficient de variation)
                    cv = (std_val / mean_val * 100) if mean_val != 0 else 0
                    
                    # Tendance (première moitié vs deuxième moitié)
                    first_half = col_data.iloc[:len(col_data)//2].mean()
                    second_half = col_data.iloc[len(col_data)//2:].mean()
                    trend = "↗️ Augmente" if second_half > first_half * 1.05 else ("↘️ Diminue" if second_half < first_half * 0.95 else "→ Stable")
                    
                    lines.append(f"\n  📊 {col}:")
                    lines.append(f"     • Étendue: {min_val:.2f} à {max_val:.2f} (variation = {max_val - min_val:.2f})")
                    lines.append(f"     • Moyenne: {mean_val:.2f} ± {std_val:.2f} (écart-type)")
                    lines.append(f"     • Médiane: {median_val:.2f}")
                    lines.append(f"     • Quartiles: Q1={q1:.2f}, Q3={q3:.2f} (IQR={q3-q1:.2f})")
                    lines.append(f"     • Variabilité: {cv:.1f}% (coef. variation)")
                    lines.append(f"     • Tendance: {trend}")
            except Exception as e:
                lines.append(f"  ❌ Erreur pour {col}: {e}")
    
    # === CORRÉLATIONS ENTRE VARIABLES ===
    if len(numeric_cols) > 1:
        try:
            corr_matrix = df[numeric_cols].corr()
            lines.append(f"\nCORRÉLATIONS ENTRE VARIABLES:")
            
            # Trouvez les paires de corrélations importantes
            important_corrs = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.3:  # Seuil de corrélation significative
                        important_corrs.append((numeric_cols[i], numeric_cols[j], corr_val))
            
            # Trier par valeur absolue
            important_corrs.sort(key=lambda x: abs(x[2]), reverse=True)
            
            if important_corrs:
                for var1, var2, corr_val in important_corrs[:10]:  # Top 10
                    strength = "Très forte" if abs(corr_val) > 0.8 else ("Forte" if abs(corr_val) > 0.6 else ("Modérée" if abs(corr_val) > 0.4 else "Faible"))
                    direction = "positive" if corr_val > 0 else "négative"
                    lines.append(f"  • {var1} ↔ {var2}: {corr_val:.3f} ({strength} {direction})")
            else:
                lines.append(f"  • Pas de corrélations notables (|r| > 0.3)")
        except Exception as e:
            lines.append(f"\nCORRÉLATIONS: Erreur - {e}")
    
    # === QUALITÉ DES DONNÉES ===
    missing_total = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()
    
    if missing_total > 0 or duplicates > 0:
        lines.append(f"\nQUALITÉ DES DONNÉES:")
        if missing_total > 0:
            pct_missing = (missing_total / (len(df) * len(df.columns))) * 100
            lines.append(f"  • Valeurs manquantes: {int(missing_total)} ({pct_missing:.1f}%)")
        if duplicates > 0:
            lines.append(f"  • Doublons: {int(duplicates)} lignes")
    
    # === COLONNES CATÉGORIQUE ===
    if categorical_cols:
        lines.append(f"\nCOLONNES CATÉGORIQUE:")
        for col in categorical_cols[:3]:  # Max 3 pour ne pas surcharger
            try:
                unique_count = df[col].nunique()
                lines.append(f"  • {col}: {unique_count} catégories uniques")
            except Exception:
                pass
    
    return "\n".join(lines)


def try_huggingface_api(question: str, df=None) -> str:
    """
    Utiliser Hugging Face Inference API - version optimisée pour stabilité
    """
    try:
        # Construire un contexte MINIMALISTE mais efficace
        context_text = ""
        if df is not None and len(df) > 0:
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            # Stats simples et rapides
            context_text = f"Rows: {len(df)}, Cols: {len(df.columns)}\n"
            
            # Juste les stats essentielles des colonnes numériques (max 3)
            for col in numeric_cols[:3]:
                try:
                    col_data = df[col].dropna()
                    if len(col_data) > 1:
                        mean_val = col_data.mean()
                        min_val = col_data.min()
                        max_val = col_data.max()
                        
                        # Tendance simple
                        first_half = col_data.iloc[:len(col_data)//2].mean()
                        second_half = col_data.iloc[len(col_data)//2:].mean()
                        trend = "UP" if second_half > first_half * 1.05 else ("DOWN" if second_half < first_half * 0.95 else "STABLE")
                        
                        context_text += f"{col}: mean={mean_val:.1f}, min={min_val:.1f}, max={max_val:.1f}, trend={trend}\n"
                except:
                    pass
        
        # API Hugging Face - modèle très léger et rapide
        url = "https://api-inference.huggingface.co/models/gpt2"
        
        # Prompt ultra-simplifié
        prompt = f"Analyze data and answer concisely (1 sentence):\n{context_text}\nQuestion: {question}\nAnswer:"
        
        headers = {"Authorization": "Bearer hf_placeholder"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 60,
                "temperature": 0.5,
            }
        }
        
        # Essayer avec timeout court d'abord
        for timeout in [15, 25]:
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=timeout)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        answer = result[0].get("generated_text", "")
                        # Extract answer after "Answer:"
                        if "Answer:" in answer:
                            answer = answer.split("Answer:")[-1]
                        answer = answer.strip()
                        if answer and len(answer) > 3:
                            return answer
                    return None
                elif response.status_code == 503:
                    # Model loading, retry with longer timeout
                    continue
                else:
                    return None
            except requests.Timeout:
                if timeout == 15:
                    continue  # Try with longer timeout
                else:
                    return None
        
        return None
    
    except Exception as e:
        print(f"HF error: {e}")
        return None


def generate_smart_response(question: str, context: str = None, df=None) -> str:
    """Générer une réponse intelligente avec les vraies données"""
    
    question_lower = question.lower()
    # Si un DataFrame est fourni, extraire les vraies valeurs
    if df is not None:
        try:
            lignes = int(len(df))
            colonnes = int(df.shape[1])
            doublons = int(df.duplicated().sum())
            missing_total = int(df.isnull().sum().sum())
            missing_by_col = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        except Exception:
            lignes = extract_number(context, "lignes")
            colonnes = extract_number(context, "colonnes")
            doublons = extract_number(context, "doublons")
            missing_total = None
            missing_by_col = None
            numeric_cols = []
    else:
        # Extraire les chiffres du contexte
        context_lower = context.lower() if context else ""
        lignes = extract_number(context, "lignes")
        colonnes = extract_number(context, "colonnes")
        doublons = extract_number(context, "doublons")
        missing_total = None
        missing_by_col = None
        numeric_cols = []
    
    # Questions sur le nombre de lignes
    if "nombre" in question_lower and "ligne" in question_lower or ("combien" in question_lower and "ligne" in question_lower):
        return f"📊 {lignes} lignes dans votre dataset."

    if ("combien" in question_lower and "colonne" in question_lower) or ("nombre" in question_lower and "colonne" in question_lower):
        return f"📋 {colonnes} colonnes dans votre dataset."
    
    # Questions sur les doublons
    if "doublon" in question_lower or "duplicate" in question_lower:
        try:
            dcount = int(doublons)
        except Exception:
            dcount = 0
        if dcount == 0:
            return "✅ Aucun doublon détecté — vos données semblent uniques."
        else:
            return f"⚠️ {dcount} doublons détectés — utilisez l'onglet 'Nettoyage' → 'Supprimer les doublons'."
    
    # Questions sur les valeurs manquantes
    if "manquant" in question_lower or "missing" in question_lower or "null" in question_lower:
        if missing_total is not None:
            # Donner les 3 colonnes les plus touchées
            top_missing = []
            if missing_by_col is not None and len(missing_by_col) > 0:
                top = missing_by_col[missing_by_col > 0].head(3)
                for col, pct in top.items():
                    top_missing.append(f"{col}: {pct:.1f}%")
            top_text = ", ".join(top_missing) if top_missing else "Aucune valeur manquante significative détectée"
            return f"💡 Total valeurs manquantes: {missing_total}. Colonnes les plus affectées: {top_text}."
        else:
            return "💡 Consultez l'onglet Analyse pour voir les valeurs manquantes par colonne."
    
    # Questions sur le nettoyage / next steps
    if "nettoyer" in question_lower or "clean" in question_lower or "problème" in question_lower:
        # Fournir recommandations concrètes si on a df
        if df is not None:
            recs = []
            if doublons and int(doublons) > 0:
                recs.append(f"Supprimer {int(doublons)} doublons")
            if missing_total and missing_total > 0:
                recs.append(f"Traiter {missing_total} valeurs manquantes (ex: mean/median/ffill)")
            if numeric_cols:
                recs.append(f"Vérifier outliers pour: {', '.join(numeric_cols[:3])}")
            if recs:
                return "🧹 Recommandations: " + "; ".join(recs)
            return "🧹 Pas d'action de nettoyage évidente — vérifiez l'onglet Analyse pour détails."
        return "🧹 Allez à l'onglet **Nettoyage** pour supprimer les doublons, outliers et valeurs manquantes."
    
    # Questions sur l'analyse
    if "analyser" in question_lower or "analyse" in question_lower:
        if df is not None and len(numeric_cols) > 0:
            sample_stats = []
            for c in numeric_cols[:3]:
                mean = df[c].mean()
                median = df[c].median()
                sample_stats.append(f"{c}⇒ mean={mean:.2f}, median={median:.2f}")
            return "📊 Exemples de stats: " + "; ".join(sample_stats)
        return "📊 L'onglet Analyse affiche les stats : min, max, moyenne, médiane par colonne."
    
    # Questions sur la visualisation
    if "visuali" in question_lower or "graphique" in question_lower or "plot" in question_lower:
        return "📈 L'onglet Visualisation permet de créer des graphiques interactifs (scatter, histogram, box, violin)."
    
    # Questions sur les prédictions
    if "prédict" in question_lower or "modèle" in question_lower or "predict" in question_lower:
        return "🤖 L'onglet Prédiction utilise un Random Forest pour classification/régression et affiche score train/test."
    
    # Questions sur la qualité
    if "qualité" in question_lower or "quality" in question_lower:
        q = f"✨ Dataset: {colonnes} colonnes, {lignes} lignes."
        if missing_total is not None:
            q += f" Valeurs manquantes: {missing_total}."
        return q + " Qualité: voir onglet Analyse pour détails."
    
    # Réponse par défaut
    return f"💡 Vous avez {lignes} lignes et {colonnes} colonnes. Explorez les onglets Analyse → Nettoyage → Visualisation pour plus de détails." 


def extract_number(text: str, keyword: str) -> str:
    """Extraire un nombre du texte basé sur un mot-clé"""
    if not text:
        return "?"
    
    # Chercher le pattern "mot-clé: nombre"
    pattern = rf"{keyword}\s*:\s*(\d+)"
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1)
    
    return "?"


def extract_text_value(text: str, keyword: str) -> str:
    """Extraire une valeur du texte basée sur un mot-clé"""
    if not text:
        return "N/A"
    
    # Chercher le pattern "mot-clé: valeur"
    pattern = rf"{keyword}\s*:\s*([^\n]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    return "N/A"
