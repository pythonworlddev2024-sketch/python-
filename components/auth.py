"""
Page d'authentification - Connexion et inscription
"""
import streamlit as st
from utils.database import create_user, verify_user


def show_auth_page():
    """Afficher la page d'authentification"""
    
    # HTML/CSS pour centrer le contenu
    st.markdown("""
        <style>
        .auth-container {
            max-width: 400px;
            margin: 10% auto;
            padding: 40px;
            border-radius: 10px;
            background-color: #f8f9fa;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        .auth-title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 30px;
            color: #3498db;
        }
        </style>
    """, unsafe_allow_html=True)
    
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
    st.subheader("🔐 Connexion")
    
    email = st.text_input("📧 Email", key="login_email", placeholder="votre@email.com")
    password = st.text_input("🔑 Mot de passe", type="password", key="login_password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Se Connecter", width='stretch', type="primary"):
            if not email or not password:
                st.error("⚠️ Veuillez remplir tous les champs")
            elif verify_user(email, password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("✅ Connexion réussie!")
                st.rerun()
            else:
                st.error("❌ Identifiants invalides")
    
    with col2:
        st.write("")  # Espace vide pour l'alignement


def show_signup():
    """Afficher le formulaire d'inscription"""
    st.subheader("✍️ Inscription")
    
    email = st.text_input("📧 Email", key="signup_email", placeholder="votre@email.com")
    password = st.text_input("🔑 Mot de passe", type="password", key="signup_password")
    password_confirm = st.text_input("🔐 Confirmer le mot de passe", type="password", key="signup_confirm")
    
    if st.button("Créer un Compte", width='stretch', type="primary"):
        if not email or not password or not password_confirm:
            st.error("⚠️ Veuillez remplir tous les champs")
        elif password != password_confirm:
            st.error("❌ Les mots de passe ne correspondent pas")
        elif len(password) < 6:
            st.error("❌ Le mot de passe doit avoir au moins 6 caractères")
        elif "@" not in email:
            st.error("❌ Veuillez entrer un email valide")
        elif create_user(email, password):
            st.success("✅ Compte créé avec succès! Connectez-vous maintenant.")
            st.rerun()
        else:
            st.error("❌ Cet email est déjà utilisé")
