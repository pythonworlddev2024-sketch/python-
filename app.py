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
    /* Variables de couleur */
    :root {
        --primary-color: #2563eb;
        --primary-dark: #1e40af;
        --primary-light: #3b82f6;
        --secondary-color: #64748b;
        --accent-color: #10b981;
        --danger-color: #ef4444;
        --warning-color: #f59e0b;
        --success-color: #10b981;
        --background-light: #f8fafc;
        --border-color: #e2e8f0;
    }
    
    /* Base Styling */
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
        background-color: #ffffff;
    }
    
    .main {
        background-color: #ffffff;
        padding: 20px 30px;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Títulos y Headings */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 {
        border-bottom: 3px solid #2563eb;
        padding-bottom: 12px;
        margin-bottom: 20px;
        font-size: 28px;
    }
    
    h2 {
        font-size: 22px;
        margin-top: 25px;
        margin-bottom: 15px;
        color: #1e293b;
    }
    
    h3 {
        font-size: 18px;
        color: #334155;
        margin-top: 15px;
        margin-bottom: 12px;
    }
    
    /* Métriques */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #2563eb;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    [data-testid="stMetric"] {
        background-color: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #2563eb;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
    }
    
    /* Boutons */
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.15);
    }
    
    .stButton > button:hover {
        background-color: #1e40af;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 15px;
        padding: 12px 24px;
        color: #64748b;
        font-weight: 600;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        color: #2563eb;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #2563eb;
        border-bottom-color: #2563eb;
    }
    
    /* Alertes et Messages */
    .stAlert {
        border-radius: 8px;
        padding: 15px 20px;
        border-left: 4px solid;
        margin: 15px 0;
    }
    
    .stWarning {
        background-color: #fef3c7;
        border-left-color: #f59e0b;
        color: #78350f;
    }
    
    .stError {
        background-color: #fee2e2;
        border-left-color: #ef4444;
        color: #7f1d1d;
    }
    
    .stSuccess {
        background-color: #d1fae5;
        border-left-color: #10b981;
        color: #065f46;
    }
    
    .stInfo {
        background-color: #dbeafe;
        border-left-color: #2563eb;
        color: #1e3a8a;
    }
    
    /* Formulaires et Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > textarea {
        border: 1px solid #e2e8f0 !important;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 14px;
        transition: all 0.3s ease;
        background-color: #f8fafc;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > textarea:focus {
        border-color: #2563eb !important;
        background-color: white;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Dividers */
    .stDivider {
        background-color: #e2e8f0;
        margin: 20px 0;
    }
    
    /* Caption et texte petit */
    .stCaption, .stText small {
        color: #64748b;
        font-size: 13px;
    }
    
    /* Dataframe */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background-color: #10b981;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
    }
    
    .stDownloadButton > button:hover {
        background-color: #059669;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }
    
    /* Containers et Sections */
    [data-testid="stVerticalBlock"] > [style*="flex-direction"] {
        gap: 15px;
    }
    
    /* Markdown personnalisé */
    .stMarkdown h4 {
        color: #334155;
        border-left: 4px solid #2563eb;
        padding-left: 12px;
        margin-top: 15px;
    }
    
    /* Animation douce au hover */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    [data-testid="column"] {
        animation: fadeIn 0.3s ease;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main {
            padding: 15px 20px;
        }
        
        h1 {
            font-size: 24px;
        }
        
        h2 {
            font-size: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

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
