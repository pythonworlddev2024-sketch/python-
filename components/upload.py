"""
Page d'importation de fichiers
"""
import streamlit as st
import pandas as pd
import os
from utils.database import get_user_data_path
from utils.data_processor import load_file, get_data_summary


def show_upload():
    """Afficher la page d'importation"""
    
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.title("📤 Importation de Données")
    with col_btn:
        if st.button("← Accueil", width='stretch'):
            st.session_state.show_upload = False
            st.rerun()
    
    st.divider()
    
    # Explication du fonctionnement
    st.markdown("""
    ### 📌 Comment utiliser cet outil ?
    
    1. **Uploadez** votre fichier CSV ou Excel
    2. **Discutez** avec notre IA pour comprendre vos données
    3. **Nettoyez** automatiquement vos données
    4. **Visualisez** et **analysez** les tendances
    5. **Prédisez** avec des modèles de machine learning
    6. **Exportez** vos résultats
    """)
    
    st.divider()
    
    # Zone d'upload au centre
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 📁 Sélectionnez votre fichier")
        
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
            
            st.success(f"✅ Fichier sauvegardé: {uploaded_file.name}")
            
            # Charger la première aperçu
            try:
                df = load_file(str(file_path))
                st.session_state.df = df
                st.session_state.df_path = str(file_path)
                
                # Afficher un aperçu
                st.subheader("📊 Aperçu des données")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lignes", len(df))
                with col2:
                    st.metric("Colonnes", len(df.columns))
                with col3:
                    st.metric("Taille", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
                
                st.dataframe(df.head(10), width="stretch")
                
                # Afficher les informations des colonnes
                st.subheader("📋 Informations des colonnes")
                col_info = pd.DataFrame({
                    "Colonne": df.columns,
                    "Type": [str(df[col].dtype) for col in df.columns],
                    "Valeurs manquantes": [df[col].isnull().sum() for col in df.columns],
                    "Uniques": [df[col].nunique() for col in df.columns]
                })
                st.dataframe(col_info, width="stretch")
                
                # Boutons d'action
                st.divider()
                
                st.success("✅ Fichier chargé avec succès! Les onglets Analyse, Nettoyage, Visualisation et Prédiction sont maintenant disponibles.")
                
                col1, col2, col3 = st.columns(3)
                
                with col2:
                    if st.button("⬆️ Importer un autre fichier", width='stretch'):
                        st.session_state.df = None
                        st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erreur lors du chargement du fichier: {str(e)}")
