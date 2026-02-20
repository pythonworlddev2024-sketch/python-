"""
Page d'importation de fichiers - Design Dark Blue AI
"""
import streamlit as st
import pandas as pd
import os
from utils.database import get_user_data_path
from utils.data_processor import load_file, get_data_summary


def show_upload():
    """Afficher la page d'importation avec design Dark Blue AI"""

    # Configuration de la page
    st.set_page_config(
        page_title="DataViz AI Analytics - Import",
        page_icon="📤",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Appliquer le thème sombre
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: #F3F4F6;
        }
        .stSidebar {
            background-color: #111827;
        }
        </style>
    """, unsafe_allow_html=True)

    # Bouton Déconnexion en haut à droite
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Déconnexion", key="logout_upload"):
            st.session_state.authenticated = False
            st.session_state.current_page = "login"
            st.rerun()

    # Titre principal centré
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Importation de Données")
        st.subheader("Chargez vos fichiers CSV ou Excel pour commencer l'analyse")

    st.divider()

    # Description claire du fonctionnement
    st.subheader("Comment ça fonctionne")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**1. Importez** votre fichier CSV ou Excel")
        st.write("**2. Analysez** avec nos outils intelligents")

    with col2:
        st.write("**3. Nettoyez** automatiquement vos données")
        st.write("**4. Visualisez** les tendances et patterns")

    with col3:
        st.write("**5. Prédisez** avec l'IA et le machine learning")
        st.write("**6. Exportez** vos résultats")

    st.divider()

    # Zone d'upload centrée
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Sélectionnez votre fichier")

        uploaded_file = st.file_uploader(
            "Déposez votre fichier ici (CSV ou Excel)",
            type=["csv", "xlsx", "xls"],
            key="file_uploader"
        )

        if uploaded_file is not None:
            # Sauvegarder le fichier
            user_path = get_user_data_path(st.session_state.user_email)
            file_path = user_path / uploaded_file.name

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Fichier sauvegardé: {uploaded_file.name}")

            # Charger la première aperçu
            try:
                df = load_file(str(file_path))
                st.session_state.df = df
                st.session_state.df_path = str(file_path)

                # Afficher un aperçu
                st.subheader("Aperçu des données")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lignes", len(df))
                with col2:
                    st.metric("Colonnes", len(df.columns))
                with col3:
                    st.metric("Taille", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")

                st.dataframe(df.head(10), use_container_width=True)

                # Afficher les informations des colonnes
                st.subheader("Informations des colonnes")
                col_info = pd.DataFrame({
                    "Colonne": df.columns,
                    "Type": [str(df[col].dtype) for col in df.columns],
                    "Valeurs manquantes": [df[col].isnull().sum() for col in df.columns],
                    "Uniques": [df[col].nunique() for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)

                # Boutons d'action
                st.divider()

                st.success("Fichier chargé avec succès ! Les onglets Analyse, Nettoyage, Visualisation et Prédiction sont maintenant disponibles.")

                col1, col2, col3 = st.columns(3)

                with col2:
                    if st.button("Importer un autre fichier", use_container_width=True):
                        st.session_state.df = None
                        st.rerun()

                # Icône IA pour déclencher discussion
                st.subheader("Discutez avec l'IA")
                if st.button("AI Assistant", key="ai_upload"):
                    with st.expander("Assistant IA", expanded=True):
                        st.write("Posez-moi une question sur vos données...")
                        user_question = st.text_input("Votre question:", key="ai_question_upload")
                        if user_question:
                            # Ici on pourrait appeler la fonction AI
                            st.write(f"Question: {user_question}")
                            st.info("Réponse de l'IA apparaîtrait ici...")
                
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
