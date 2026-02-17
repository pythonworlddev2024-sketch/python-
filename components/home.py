"""
Page d'accueil avec animation et bouton de démarrage
"""
import streamlit as st


def show_home():
    """Afficher la page d'accueil"""
    
    # CSS pour les animations
    st.markdown("""
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .title-container {
            text-align: center;
            animation: fadeIn 0.8s ease-in;
            padding: 60px 20px;
        }
        
        .main-title {
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(135deg, #3498db, #2ecc71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        
        .subtitle {
            font-size: 20px;
            color: #7f8c8d;
            margin-bottom: 40px;
            line-height: 1.6;
        }
        
        .cta-button {
            display: inline-block;
            padding: 15px 50px;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 18px;
            font-weight: bold;
            animation: pulse 2s infinite;
            transition: transform 0.3s;
        }
        
        .cta-button:hover {
            transform: scale(1.1);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 60px 0;
            animation: fadeIn 1.2s ease-in;
        }
        
        .feature-card {
            padding: 25px;
            border-radius: 10px;
            background: linear-gradient(135deg, #ecf0f1, #bdc3c7);
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 40px;
            margin-bottom: 15px;
        }
        
        .feature-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .feature-description {
            font-size: 14px;
            color: #555;
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Titre et sous-titre animés
    st.markdown("""
        <div class="title-container">
            <h1 class="main-title">📊 DataViz AI Analytics</h1>
            <p class="subtitle">
                Transformez vos données brutes en insights actionnables<br>
                Analyse intelligente • Prédictions précises • Interface intuitive
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Bouton de démarrage
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Commencer", width='stretch', type="primary", key="btn_start"):
            st.session_state.show_upload = True
            st.rerun()
    
    st.divider()
    
    # Fonctionnalités
    st.markdown("""
        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">📤</div>
                <div class="feature-title">Import Facile</div>
                <div class="feature-description">Importez vos fichiers CSV ou Excel en un clic</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧹</div>
                <div class="feature-title">Nettoyage Automique</div>
                <div class="feature-description">Supprimez doublons et valeurs aberrantes</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Visualisation</div>
                <div class="feature-description">Graphiques interactifs et professionnels</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">IA Gratuite</div>
                <div class="feature-description">Predictions et conseils alimentés par l'IA</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💡</div>
                <div class="feature-title">Insights Intelligents</div>
                <div class="feature-description">Recommandations basées sur vos données</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📥</div>
                <div class="feature-title">Téléchargement</div>
                <div class="feature-description">Exportez vos données nettoyées et rapports</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Section supplémentaire
    st.markdown("""
        <div style="text-align: center; margin-top: 60px; padding: 30px; background: #f8f9fa; border-radius: 10px;">
            <h3 style="color: #3498db;">Comment ça fonctionne ?</h3>
            <p style="font-size: 16px; color: #555; line-height: 1.8;">
                <strong>1. Importez</strong> vos données (CSV ou Excel)<br>
                <strong>2. Analysez</strong> avec nos outils de nettoyage<br>
                <strong>3. Visualisez</strong> vos données avec des graphiques interactifs<br>
                <strong>4. Prédisez</strong> en utilisant l'IA et le machine learning<br>
                <strong>5. Exportez</strong> vos résultats et rapports
            </p>
        </div>
    """, unsafe_allow_html=True)
