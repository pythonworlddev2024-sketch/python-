"""
Page d'authentification - Design Dark Blue AI
"""
import streamlit as st
from utils.database import create_user, verify_user


def show_auth_page():
    """Afficher la page d'authentification avec design Dark Blue AI"""

    # Configuration de la page
    st.set_page_config(
        page_title="DataViz AI Analytics - Login",
        page_icon="🔐",
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

    # Entête professionnelle centrée
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("DataViz AI Analytics")
        st.subheader("Intelligence Artificielle pour l'Analyse de Données")
        st.write("Transformez vos données en insights actionnables")

    st.divider()

    # Créer deux colonnes pour les onglets
    col1, col2 = st.columns(2)

    with col1:
        auth_mode = st.radio("Mode d'authentification", ["Connexion", "Inscription"], horizontal=True, label_visibility="collapsed")

    st.divider()

    if auth_mode == "Connexion":
        show_login()
    else:
        show_signup()


def show_login():
    """Afficher le formulaire de connexion"""
    st.subheader("Connexion")

    email = st.text_input("Gmail", key="login_email", placeholder="votre.email@gmail.com")
    password = st.text_input("Mot de passe", type="password", key="login_password")

    # Bouton centré
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Se connecter", type="primary", use_container_width=True):
            if not email or not password:
                st.error("Veuillez remplir tous les champs")
            elif verify_user(email, password):
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.current_page = "upload"
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Identifiants invalides. Vérifiez votre email et mot de passe.")


def show_signup():
    """Afficher le formulaire d'inscription"""
    st.subheader("Inscription")

    email = st.text_input("Gmail", key="signup_email", placeholder="votre.email@gmail.com")
    password = st.text_input("Mot de passe", type="password", key="signup_password")
    password_confirm = st.text_input("Confirmer le mot de passe", type="password", key="signup_confirm")

    if st.button("Créer un Compte", type="primary", use_container_width=True):
        if not email or not password or not password_confirm:
            st.error("Veuillez remplir tous les champs")
        elif password != password_confirm:
            st.error("Les mots de passe ne correspondent pas")
        elif len(password) < 6:
            st.error("Le mot de passe doit avoir au moins 6 caractères")
        elif "@" not in email or ".com" not in email:
            st.error("Veuillez entrer un email Gmail valide")
        elif create_user(email, password):
            st.success("Compte créé avec succès ! Connectez-vous maintenant.")
            st.rerun()
        else:
            st.error("Cet email est déjà utilisé. Un utilisateur = un seul compte.")
