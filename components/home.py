"""
Page d'accueil avec design professionnel Dark Blue AI
"""
import streamlit as st


def show_home():
    """Afficher la page d'accueil avec design Dark Blue AI"""

    # Configuration de la page
    st.set_page_config(
        page_title="DataViz AI Analytics",
        page_icon="📊",
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
        if st.button("Déconnexion", key="logout_home"):
            st.session_state.authenticated = False
            st.session_state.current_page = "login"
            st.rerun()

    # Titre principal centré
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("DataViz AI Analytics")
        st.subheader("Transformez vos données brutes en insights actionnables")
        st.subheader("Analyse intelligente • Prédictions précises • Interface intuitive")

    # Bouton Start centré
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start", type="primary", use_container_width=True):
            st.session_state.current_page = "login"
            st.rerun()

    st.divider()

    # Fonctionnalités
    st.subheader("Fonctionnalités principales")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Import Facile")
        st.write("Importez vos fichiers CSV ou Excel en un clic")

        st.markdown("### Nettoyage Automatique")
        st.write("Supprimez doublons et valeurs aberrantes")

    with col2:
        st.markdown("### Visualisation")
        st.write("Graphiques interactifs et professionnels")

        st.markdown("### IA Gratuite")
        st.write("Predictions et conseils alimentés par l'IA")

    with col3:
        st.markdown("### Insights Intelligents")
        st.write("Recommandations basées sur vos données")

        st.markdown("### Téléchargement")
        st.write("Exportez vos données nettoyées et rapports")

    # Section "Comment ça fonctionne"
    st.subheader("Comment ça fonctionne ?")

    st.write("""
    1. **Importez** vos données (CSV ou Excel)
    2. **Analysez** avec nos outils de nettoyage
    3. **Visualisez** vos données avec des graphiques interactifs
    4. **Prédisez** en utilisant l'IA et le machine learning
    5. **Exportez** vos résultats et rapports
    """)

    # Bouton AI flottant en bas à droite (simulé avec columns)
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🤖 AI", key="ai_button_home"):
            with st.expander("Assistant IA", expanded=True):
                st.write("Posez-moi une question sur vos données...")
                user_question = st.text_input("Votre question:", key="ai_question_home")
                if user_question:
                    # Ici on pourrait appeler la fonction AI
                    st.write(f"Question: {user_question}")
                    st.info("Réponse de l'IA apparaîtrait ici...")
