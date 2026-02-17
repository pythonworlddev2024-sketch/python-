"""
Application Streamlit - DataViz AI Analytics
Application web pour l'analyse de données et la prédiction avec IA gratuite
"""

import streamlit as st
from config import APP_TITLE, APP_ICON

# Configuration de la page Streamlit
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background-color: #ffffff;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #3498db;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #7f8c8d;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
        padding-left: 30px;
        padding-right: 30px;
    }
    
    .stAlert {
        padding-left: 30px;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #34495e;
    }
    
    h3 {
        color: #7f8c8d;
    }
    </style>
""", unsafe_allow_html=True)

# Initialiser les variables de session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.page = "home"
    st.session_state.df = None
    st.session_state.df_path = None

# Barre latérale
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #3498db; border: none; font-size: 32px;">{APP_ICON} {APP_TITLE}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.session_state.logged_in:
        st.markdown(f"👤 **Utilisateur:** `{st.session_state.user_email}`")
        st.divider()
        
        # Navigation
        st.markdown("### 📍 Navigation")
        
        if st.button("🎪s Accueil", width='stretch'):
            st.session_state.page = "home"
            st.rerun()
        
        if st.button("📤 Importer", width='stretch'):
            st.session_state.page = "upload"
            st.rerun()
        
        if st.session_state.df is not None:
            if st.button("🧹 Nettoyer", width='stretch'):
                st.session_state.page = "cleaning"
                st.rerun()
            
            if st.button("📈 Visualiser", width='stretch'):
                st.session_state.page = "visualization"
                st.rerun()
        
        st.divider()
        
        # Informations sur les données
        if st.session_state.df is not None:
            st.markdown("### 📊 Données Chargées")
            st.metric("Lignes", len(st.session_state.df))
            st.metric("Colonnes", len(st.session_state.df.columns))
        
        st.divider()
        
        # Déconnexion
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.df = None
            st.session_state.page = "home"
            st.rerun()
    
    st.divider()
    
    # Information sur l'application
    st.markdown("""
    ### 📚 À Propos
    
    **DataViz AI Analytics** est une application web complète pour:
    
    - 📤 Importer et gérer vos données
    - 🧹 Nettoyer automatiquement vos données
    - 📈 Créer des visualisations interactives
    - 🤖 Faire des prédictions avec IA
    - 📥 Exporter vos résultats
    
    ---
    
    **Développé avec:**
    - 🐍 Python & Streamlit
    - 📊 Pandas & Plotly
    - 🤖 Scikit-learn
    - 🧠 IA Gratuite (Hugging Face / Groq)
    """)

# ============== CONTENU PRINCIPAL ==============

if not st.session_state.logged_in:
    # Page d'authentification
    from pages.auth import show_auth_page
    show_auth_page()

else:
    # Navigation globale avec onglets
    from pages.home import show_home
    from pages.upload import show_upload
    from pages.cleaning import show_cleaning_content
    from pages.visualization import show_visualization_content
    
    # Onglets principaux
    if st.session_state.df is None:
        # Avant l'importation, afficher Accueil et Importation
        tab_home, tab_upload = st.tabs(["🏠 Accueil", "📤 Importation"])
        
        with tab_home:
            show_home()
        
        with tab_upload:
            show_upload()
    
    else:
        # Après l'importation, afficher tous les onglets
        tab_analysis, tab_cleaning, tab_viz, tab_predict = st.tabs([
            "📊 Analyse",
            "🧹 Nettoyage",
            "📈 Visualisation",
            "🤖 Prédiction"
        ])
        
        with tab_analysis:
            show_cleaning_content(tab_type="analysis")
        
        with tab_cleaning:
            show_cleaning_content(tab_type="cleaning")
        
        with tab_viz:
            show_visualization_content(tab_type="visualization")
        
        with tab_predict:
            show_visualization_content(tab_type="prediction")

# Pied de page
st.divider()

st.markdown("""
    <div style="text-align: center; padding: 20px; color: #7f8c8d; font-size: 12px;">
        <p>
        DataViz AI Analytics © 2025 | 
        <a href="#" style="color: #3498db; text-decoration: none;">Support</a> | 
        <a href="#" style="color: #3498db; text-decoration: none;">FAQ</a> | 
        <a href="#" style="color: #3498db; text-decoration: none;">Politique de Confidentialité</a>
        </p>
        <p>Créé avec ❤️ pour l'analyse de données intelligente</p>
    </div>
""", unsafe_allow_html=True)
