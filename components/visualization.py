"""
Page de visualisation et prédiction
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ml_model import PredictionModel


def show_visualization():
    """Afficher la page de visualisation (ancienne structure)"""
    
    if st.session_state.df is None:
        st.warning("⚠️ Aucun fichier importé. Veuillez d'abord importer un fichier.")
        if st.button("Retour à l'importation"):
            st.session_state.page = "upload"
            st.rerun()
        return
    
    st.title("📈 Visualisation et Prédiction")
    
    # Navigation
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Retour au Nettoyage", width='stretch'):
            st.session_state.page = "cleaning"
            st.rerun()
    
    st.divider()
    
    # Onglets
    tabs = st.tabs(["📊 Visualisation Interactive", "🤖 Prédictions"])
    
    with tabs[0]:
        show_visualization_tab()
    
    with tabs[1]:
        show_prediction_tab()


def show_visualization_content(tab_type="visualization"):
    """Afficher le contenu de visualisation dans les onglets globaux"""
    
    if st.session_state.df is None:
        st.warning("⚠️ Aucun fichier importé. Veuillez d'abord importer un fichier.")
        return
    
    if tab_type == "visualization":
        show_visualization_tab()
    elif tab_type == "prediction":
        show_prediction_tab()


def show_visualization_tab():
    """Afficher les visualisations interactives"""
    
    st.subheader("📊 Visualisation Interactive")
    
    df = st.session_state.df
    
    # Sélection des variables
    col1, col2 = st.columns(2)
    
    with col1:
        selected_vars = st.multiselect(
            "Sélectionnez les variables à visualiser",
            df.columns.tolist(),
            default=df.columns.tolist()[:2] if len(df.columns) >= 2 else df.columns.tolist(),
            key="viz_vars"
        )
    
    with col2:
        chart_type = st.selectbox(
            "Type de graphique",
            ["Scatter", "Line", "Bar", "Histogram", "Box", "Violin"],
            key="chart_type"
        )
    
    if selected_vars:
        df_filtered = df[selected_vars]
        
        # Générer le graphique approprié
        if chart_type == "Scatter" and len(selected_vars) >= 2:
            fig = px.scatter(df, x=selected_vars[0], y=selected_vars[1], 
                           title=f"{selected_vars[0]} vs {selected_vars[1]}")
            st.plotly_chart(fig, width="stretch")
            
            # Description
            st.info(f"📌 Ce graphique montre la relation entre {selected_vars[0]} et {selected_vars[1]}")
        
        elif chart_type == "Line" and len(selected_vars) >= 2:
            fig = px.line(df, x=selected_vars[0], y=selected_vars[1],
                         title=f"Tendance - {selected_vars[1]} par {selected_vars[0]}")
            st.plotly_chart(fig, width="stretch")
        
        elif chart_type == "Bar" and len(selected_vars) >= 2:
            fig = px.bar(df, x=selected_vars[0], y=selected_vars[1],
                        title=f"Comparaison - {selected_vars[0]} vs {selected_vars[1]}")
            st.plotly_chart(fig, width="stretch")
        
        elif chart_type == "Histogram":
            for var in selected_vars:
                if pd.api.types.is_numeric_dtype(df[var]):
                    fig = px.histogram(df, x=var, nbins=30, title=f"Distribution - {var}")
                    st.plotly_chart(fig, width="stretch")
        
        elif chart_type == "Box":
            for var in selected_vars:
                if pd.api.types.is_numeric_dtype(df[var]):
                    fig = px.box(df, y=var, title=f"Boxplot - {var}")
                    st.plotly_chart(fig, width="stretch")
        
        elif chart_type == "Violin":
            for var in selected_vars:
                if pd.api.types.is_numeric_dtype(df[var]):
                    fig = px.violin(df, y=var, title=f"Violin Plot - {var}")
                    st.plotly_chart(fig, width="stretch")
        
        else:
            st.warning("⚠️ Sélection invalide pour ce type de graphique")


def show_prediction_tab():
    """Afficher le module de prédiction"""
    
    st.subheader("🤖 Module de Prédiction")
    
    df = st.session_state.df
    
    # Sélection de la variable cible
    target_col = st.selectbox(
        "Sélectionnez la variable à prédire",
        df.columns.tolist(),
        key="target_col"
    )
    
    if target_col:
        st.divider()
        
        # Entraîner le modèle
        st.info("🔧 Entraînement du modèle en cours...")
        
        model = PredictionModel(df, target_col)
        scores = model.train()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Score Entraînement", f"{scores['train_score']:.2%}")
        
        with col2:
            st.metric("Score Test", f"{scores['test_score']:.2%}")
        
        st.divider()
        
        # Formulaire de prédiction
        st.subheader("🔮 Faire une Prédiction")
        
        # Récupérer les colonnes de features
        feature_cols = [col for col in df.columns if col != target_col]
        
        input_data = {}
        
        col1, col2 = st.columns(2)
        
        for i, col in enumerate(feature_cols):
            if i % 2 == 0:
                container = col1
            else:
                container = col2
            
            with container:
                if pd.api.types.is_numeric_dtype(df[col]):
                    min_val = float(df[col].min())
                    max_val = float(df[col].max())
                    input_data[col] = st.slider(
                        f"📊 {col}",
                        min_value=min_val,
                        max_value=max_val,
                        value=float(df[col].mean()),
                        key=f"pred_{col}"
                    )
                else:
                    unique_vals = df[col].unique().tolist()
                    input_data[col] = st.selectbox(
                        f"📋 {col}",
                        unique_vals,
                        key=f"pred_{col}"
                    )
        
        st.divider()
        
        # Bouton de prédiction
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🌯 Valider et Prédire", width='stretch', type="primary"):
                # Vérifier qu'au moins un champ est rempli
                if all(v for v in input_data.values()):
                    try:
                        prediction = model.predict(input_data)
                        
                        st.success("✅ Prédiction générée!")
                        
                        # Afficher le résultat
                        st.markdown(f"""
                        <div style="text-align: center; padding: 30px; background: #f0f9ff; border-radius: 10px; border-left: 5px solid #3498db;">
                            <h2 style="color: #3498db;">Prédiction pour {target_col}</h2>
                            <h1 style="color: #2ecc71; font-size: 48px; font-weight: bold;">{prediction}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Importance des features
                        st.subheader("📊 Importance des Features")
                        
                        importance = model.get_feature_importance()
                        importance_df = pd.DataFrame(list(importance.items()), 
                                                    columns=['Feature', 'Importance'])
                        importance_df = importance_df.sort_values('Importance', ascending=False)
                        
                        fig = px.bar(importance_df, x='Feature', y='Importance',
                                   title="Importance relative des variables")
                        st.plotly_chart(fig, width="stretch")
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la prédiction: {str(e)}")
                else:
                    st.warning("⚠️ Veuillez remplir tous les champs")
