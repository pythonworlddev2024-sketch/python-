"""
Application Streamlit - DataViz AI Analytics
Application web pour l'analyse de données et la prédiction avec IA gratuite
"""

import streamlit as st
from config import APP_TITLE, APP_ICON

# Initialize session state for API key
if "google_api_key" not in st.session_state:
    st.session_state.google_api_key = ""

# Try to load from Streamlit secrets first
if not st.session_state.google_api_key:
    api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("google", {}).get("api_key") or ""
    if api_key:
        st.session_state.google_api_key = api_key

# Optional: Allow user to enter API key for faster/better AI responses
if not st.session_state.google_api_key:
    with st.expander("(Optionnel) Activer Google Gemini pour des réponses IA plus rapides"):
        st.info("L'IA fonctionne déjà gratuitement. Entrez une clé Google Gemini API pour des réponses plus rapides et de meilleure qualité.")
        api_key_input = st.text_input(
            "Google API Key (Gemini)",
            type="password",
            placeholder="AIzaSy...",
            help="Facultatif. Votre clé sera stockée en session seulement."
        )
        if api_key_input:
            st.session_state.google_api_key = api_key_input
            st.success("Clé Gemini activée !")

# Configuration de la page Streamlit
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser les variables de session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.df = None
    st.session_state.df_path = None
    st.session_state.show_upload = False

# ============== CONTENU PRINCIPAL ==============

if not st.session_state.logged_in:
    # Page d'authentification
    from components.auth import show_auth_page
    show_auth_page()

else:
    # Importer le chat flottant
    from components.chat import show_floating_chat
    
    # Afficher le chat sur le sidebar (accessible partout!)
    show_floating_chat()
    
    # Navigation globale avec onglets
    from components.home import show_home
    from components.upload import show_upload
    from components.cleaning import show_cleaning_content
    from components.visualization import show_visualization_content
    
    # En-tête avec infos utilisateur
    col_title, col_spacer, col_user = st.columns([1, 2, 1])
    with col_title:
        st.markdown(f"### {APP_ICON} {APP_TITLE}")
    with col_user:
        col_info, col_logout = st.columns([2, 1])
        with col_info:
            if st.session_state.df is not None:
                st.caption(f"👤 {st.session_state.user_email}")
        with col_logout:
            if st.button("🚪 Déconv.", width='stretch'):
                st.session_state.logged_in = False
                st.session_state.user_email = None
                st.session_state.df = None
                st.rerun()
    
    st.divider()
    
    # Onglets principaux
    if st.session_state.df is None:
        # Avant l'importation, afficher Accueil et Importation
        if st.session_state.show_upload:
            # Afficher directement l'onglet d'importation
            show_upload()
        else:
            # Afficher avec les deux onglets
            tab_home, tab_upload = st.tabs(["🏠 Accueil", "📤 Importation"])
            
            with tab_home:
                show_home()
            
            with tab_upload:
                show_upload()
    
    else:
        # Réinitialiser le flag après l'importation
        st.session_state.show_upload = False
        
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
        
        st.divider()
        
        # Bouton pour importer un nouveau fichier
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if st.button("📤 Importer nouveau fichier", width='stretch'):
                st.session_state.df = None
                st.rerun()

# Pied de page
st.divider()

st.markdown("""
    <div style="text-align: center; padding: 15px; color: #7f8c8d; font-size: 11px;">
        <p>DataViz AI Analytics © 2025 | Créé avec ❤️ pour l'analyse de données</p>
    </div>
""", unsafe_allow_html=True)
