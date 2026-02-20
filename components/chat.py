"""
Composant de chatbot flottant accessible partout
"""
import streamlit as st
from utils.data_processor import get_data_summary
from utils.ai_helper import get_ai_response


def show_floating_chat():
    """Afficher le chat flottant sur la barre latérale avec vraies données"""

    with st.sidebar:
        st.divider()

        # Titre du chat
        st.markdown("### Assistant IA")

        # Vérifier si un fichier est chargé
        if st.session_state.df is not None:
            df = st.session_state.df
            summary = get_data_summary(df)

            # Afficher les stats rapidement
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Lignes", summary['rows'])
            with col2:
                st.metric("Colonnes", summary['columns'])

            # Zone de saisie
            question = st.text_input(
                "Posez une question...",
                key="sidebar_chat_input",
                placeholder="Ex: Combien de lignes? Doublons?"
            )

            if question:
                # Créer un contexte DÉTAILLÉ avec vraies données
                context = f"""Résumé détaillé des données:
lignes: {summary['rows']}
colonnes: {summary['columns']}
doublons: {summary['duplicates']}
valeurs manquantes: {summary['missing_values']}
mémoire: {summary['memory_usage']} MB
colonnes présentes: {', '.join(df.columns.tolist())}"""

                # Obtenir la réponse intelligente
                with st.spinner("Réflexion..."):
                    response = get_ai_response(question, context, df)

                # Afficher la réponse
                st.success(response)

            # Bouton pour plus d'info
            if st.button("Activer l'IA Groq Premium", use_container_width=True):
                st.info("""
                **Groq - IA Gratuite & Ultra-Rapide**

                1. Allez sur: https://console.groq.com/keys
                2. Créez un compte gratuit
                3. Générez une clé API
                4. Puis dans Terminal:
                ```bash
                export GROQ_API_KEY="votre_clé"
                streamlit run app.py
                ```
                """)

        else:
            st.info("Importez un fichier pour utiliser l'IA")

        st.divider()
