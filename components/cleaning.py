"""
Page de nettoyage et analyse des données
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils.data_processor import (
    remove_duplicates, handle_outliers, fill_missing_values, get_column_stats
)
from utils.report_generator import ReportGenerator
from utils.data_exporter import DataExporter


def show_cleaning():
    """Afficher la page de nettoyage (ancienne structure)"""
    
    if st.session_state.df is None:
        st.warning("⚠️ Aucun fichier importé. Veuillez d'abord importer un fichier.")
        if st.button("Retour à l'importation"):
            st.session_state.page = "upload"
            st.rerun()
        return
    
    st.title("🧹 Nettoyage et Analyse des Données")
    
    # Informations utilisateur
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Retour à l'importation", width='stretch'):
            st.session_state.page = "upload"
            st.rerun()
    
    st.divider()
    
    # Onglets
    tabs = st.tabs(["📊 Analyse", "🧹 Nettoyage", "📥 Export"])
    
    # ============== ONGLET ANALYSE ==============
    with tabs[0]:
        show_analysis_tab()
    
    # ============== ONGLET NETTOYAGE ==============
    with tabs[1]:
        show_cleaning_tab()
    
    # ============== ONGLET EXPORT ==============
    with tabs[2]:
        show_export_tab()


def show_cleaning_content(tab_type="analysis"):
    """Afficher le contenu de nettoyage dans les onglets globaux"""
    
    if st.session_state.df is None:
        st.warning("⚠️ Aucun fichier importé. Veuillez d'abord importer un fichier.")
        return
    
    if tab_type == "analysis":
        show_analysis_tab()
    elif tab_type == "cleaning":
        show_cleaning_tab()
    elif tab_type == "export":
        show_export_tab()


def show_analysis_tab():
    """Afficher l'onglet d'analyse"""
    
    st.subheader("📈 Résumé des Données")
    
    df = st.session_state.df
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Lignes", len(df))
    
    with col2:
        st.metric("📋 Colonnes", len(df.columns))
    
    with col3:
        st.metric("🔄 Doublons", df.duplicated().sum())
    
    with col4:
        st.metric("⚠️ Manquants", df.isnull().sum().sum())
    
    st.divider()
    
    # Détails des colonnes
    st.subheader("📋 Détails des Colonnes")
    
    col_stats = get_column_stats(df)
    
    stats_list = []
    for col_name, stats in col_stats.items():
        if stats["type"] == "Quantitative":
            stats_list.append({
                "Colonne": col_name,
                "Type": "Quantitative",
                "Min": f"{stats['min']:.2f}" if isinstance(stats['min'], (int, float)) else stats['min'],
                "Max": f"{stats['max']:.2f}" if isinstance(stats['max'], (int, float)) else stats['max'],
                "Moyenne": f"{stats['mean']:.2f}" if pd.notna(stats['mean']) else "N/A",
                "Médiane": f"{stats['median']:.2f}" if pd.notna(stats['median']) else "N/A",
                "Manquants": stats['null_count'],
                "Remarque": stats.get('remark') if stats.get('remark') else ""
            })
        else:
            stats_list.append({
                "Colonne": col_name,
                "Type": "Qualitative",
                "Valeurs Uniques": stats['unique_values'],
                "Plus Commun": stats['most_common'],
                "Manquants": stats['null_count'],
                "Remarque": ""
            })
    
    df_stats = pd.DataFrame(stats_list)
    st.dataframe(df_stats, width="stretch")
    
    st.divider()
    
    # Distribution des variables
    st.subheader("📊 Distribution des Variables")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        col_to_plot = st.selectbox("Sélectionnez une colonne", numeric_cols, key="analysis_histogram")
        
        fig = px.histogram(df, x=col_to_plot, nbins=30, title=f"Distribution de {col_to_plot}")
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Aucune colonne numérique trouvée")
    
    st.divider()
    
    # Aperçu des premières lignes
    st.subheader("👀 Aperçu des Données")
    
    n_rows = st.slider("Nombre de lignes à afficher", 1, min(50, len(df)), 10)
    st.dataframe(df.head(n_rows), width="stretch")
    
    st.divider()
    st.markdown("### 💾 Télécharger le Rapport d'Analyse (PDF)")
    report_gen = ReportGenerator(df, filename="dataset_analysis")
    try:
        pdf_report = report_gen.generate_pdf_report()
        if pdf_report:
            pdf_bytes = pdf_report.getvalue() if hasattr(pdf_report, 'getvalue') else pdf_report
            st.download_button(
                label="📥 Télécharger le rapport (PDF)",
                data=pdf_bytes,
                file_name="rapport_analyse.pdf",
                mime="application/pdf",
                width='stretch'
            )
            # Save server-side copy
            try:
                with open('reports/rapport_analyse_analysis.pdf', 'wb') as f:
                    f.write(pdf_bytes)
            except Exception as e:
                st.warning(f"⚠️ Impossible d'enregistrer la copie serveur: {e}")
        else:
            st.warning("⚠️ PDF indisponible")
    except Exception as e:
        st.error(f"❌ Erreur génération PDF: {e}")


def show_cleaning_tab():
    """Afficher l'onglet de nettoyage"""
    
    st.subheader("🧹 Actions de Nettoyage")
    
    df = st.session_state.df
    original_len = len(df)
    
    # === SECTION 1: SUPPRIMER LES DOUBLONS ===
    st.markdown("#### 🔄 Étape 1: Supprimer les Doublons")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        duplicates_count = df.duplicated().sum()
        if duplicates_count > 0:
            st.warning(f"⚠️ {duplicates_count} doublons détectés dans vos données")
        else:
            st.success("✅ Aucun doublon détecté")
    
    with col2:
        if st.button("🔄 Supprimer les doublons", width='stretch'):
            if duplicates_count > 0:
                df_cleaned, removed_rows = remove_duplicates(df)
                st.session_state.df = df_cleaned
                st.success(f"✅ {removed_rows} doublons supprimés")
                st.rerun()
    
    st.divider()
    
    # === SECTION 2: VALEURS MANQUANTES ===
    st.markdown("#### 📝 Étape 2: Traiter les Valeurs Manquantes")
    
    missing_total = df.isnull().sum().sum()
    
    if missing_total > 0:
        st.warning(f"⚠️ {int(missing_total)} valeurs manquantes détectées")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            method = st.selectbox(
                "Sélectionnez la méthode de traitement",
                ["mean", "median", "forward_fill"],
                format_func=lambda x: {
                    "mean": "📊 Moyenne",
                    "median": "📈 Médiane",
                    "forward_fill": "➡️ Forward Fill"
                }[x],
                key="fill_method"
            )
        
        with col3:
            if st.button("📝 Remplir", width='stretch'):
                df_filled = fill_missing_values(st.session_state.df, method=method)
                st.session_state.df = df_filled
                st.success(f"✅ Valeurs manquantes traitées avec: {method}")
                st.rerun()
    else:
        st.success("✅ Aucune valeur manquante détectée")
    
    st.divider()
    
    # === SECTION 3: VALEURS ABERRANTES ===
    st.markdown("#### 📊 Étape 3: Gérer les Valeurs Aberrantes (Outliers)")
    
    numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_cols:
        col_to_clean = st.selectbox(
            "Sélectionnez une colonne numérique à analyser",
            numeric_cols,
            key="outlier_col"
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Afficher le boxplot
            fig = px.box(
                st.session_state.df,
                y=col_to_clean,
                title=f"Distribution - {col_to_clean}",
                color_discrete_sequence=["#2563eb"]
            )
            fig.update_layout(
                height=400,
                template="plotly_white",
                font=dict(size=12)
            )
            st.plotly_chart(fig, width="stretch")
        
        with col2:
            outliers_stats = st.session_state.df[col_to_clean].describe()
            st.metric("Min", f"{outliers_stats['min']:.2f}")
            st.metric("Q1", f"{st.session_state.df[col_to_clean].quantile(0.25):.2f}")
            st.metric("Médiane", f"{outliers_stats['50%']:.2f}")
            st.metric("Q3", f"{st.session_state.df[col_to_clean].quantile(0.75):.2f}")
            st.metric("Max", f"{outliers_stats['max']:.2f}")
            
            if st.button("🛡️ Supprimer Outliers", width='stretch'):
                df_cleaned = handle_outliers(st.session_state.df, col_to_clean)
                rows_removed = len(st.session_state.df) - len(df_cleaned)
                st.session_state.df = df_cleaned
                st.success(f"✅ {rows_removed} valeurs aberrantes supprimées")
                st.rerun()
    else:
        st.info("ℹ️ Aucune colonne numérique trouvée pour l'analyse des outliers")
    
    st.divider()
    
    # === RÉSUMÉ APRÈS NETTOYAGE ===
    st.markdown("### ✅ Résumé Après Nettoyage")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Lignes", len(st.session_state.df))
    
    with col2:
        st.metric("📋 Colonnes", len(st.session_state.df.columns))
    
    with col3:
        st.metric("🔄 Doublons", st.session_state.df.duplicated().sum())
    
    with col4:
        st.metric("⚠️ Manquants", st.session_state.df.isnull().sum().sum())
    
    st.divider()
    
    # === TÉLÉCHARGER LES DONNÉES NETTOYÉES ===
    st.markdown("### 📥 Télécharger les Données Nettoyées")
    
    try:
        df = st.session_state.df
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📄 CSV**")
            csv_data = DataExporter.to_csv(df)
            if csv_data:
                st.download_button(
                    label="📥 Télécharger en CSV",
                    data=csv_data,
                    file_name="donnees_nettoyees.csv",
                    mime="text/csv",
                    width='stretch'
                )
        
        with col2:
            st.markdown("**📊 Excel**")
            excel_buffer = DataExporter.to_excel(df)
            if excel_buffer:
                st.download_button(
                    label="📥 Télécharger en Excel",
                    data=excel_buffer,
                    file_name="donnees_nettoyees.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
    except Exception as e:
        st.error(f"❌ Erreur lors de l'export: {str(e)}")


def show_export_tab():
    """Afficher l'onglet d'export avec rapport professionnel"""
    
    df = st.session_state.df
    
    if df is None or df.empty:
        st.warning("⚠️ Aucune donnée à exporter. Veuillez d'abord importer un fichier.")
        return
    
    # ========== SECTION 1: RAPPORT D'ANALYSE ==========
    st.subheader("📊 Rapport d'Analyse Après Nettoyage")
    
    # Onglets pour rapport
    tab_report, tab_download = st.tabs(["📋 Rapport", "💾 Télécharger Rapport"])
    
    with tab_report:
        try:
            show_report_section()
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération du rapport: {str(e)}")
    
    with tab_download:
        try:
            show_report_download_section()
        except Exception as e:
            st.error(f"❌ Erreur lors de la préparation du téléchargement: {str(e)}")
    
    st.divider()
    
    # ========== SECTION 2: EXPORT DES DONNÉES NETTOYÉES ==========
    st.subheader("📥 Télécharger les Données Nettoyées")
    
    try:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📄 Export en CSV")
            csv_data = DataExporter.to_csv(df)
            if csv_data:
                st.download_button(
                    label="📥 Télécharger en CSV",
                    data=csv_data,
                    file_name="donnees_nettoyees.csv",
                    mime="text/csv",
                    width='stretch'
                )
            st.caption("Format standard pour Excel, Google Sheets, etc.")
        
        with col2:
            st.markdown("### 📊 Export en Excel")
            excel_buffer = DataExporter.to_excel(df)
            if excel_buffer:
                st.download_button(
                    label="📥 Télécharger en Excel",
                    data=excel_buffer,
                    file_name="donnees_nettoyees.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
            st.caption("Format Excel avec feuille 'Résumé' des statistiques")
    except Exception as e:
        st.error(f"❌ Erreur lors de l'export des données: {str(e)}")
    
    st.divider()
    
    # ========== SECTION 3: RÉSUMÉ FINAL ==========
    st.subheader("✅ Résumé du Nettoyage")
    
    try:
        info_export = DataExporter.get_export_info(df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Lignes", f"{info_export['lignes']:,}")
        
        with col2:
            st.metric("📋 Colonnes", info_export['colonnes'])
        
        with col3:
            st.metric("✨ Qualité", f"{info_export['completness_pct']:.1f}%")
        
        with col4:
            st.metric("⚠️ Manquants", info_export['missing_total'])
        
        st.info(f"""
        ✅ **Données nettoyées et prêtes à l'emploi!**
        
        📊 Votre dataset contient maintenant **{info_export['lignes']:,} lignes** et **{info_export['colonnes']} colonnes**
        
        🔍 Complétude des données: **{info_export['completness_pct']:.1f}%**
        
        💾 Vous pouvez maintenant:
        - Télécharger les données nettoyées en CSV ou Excel
        - Utiliser les données pour la visualisation
        - Entraîner des modèles de machine learning
        """)
        
        st.divider()
        
        # Navigation
        col_left, col_center, col_right = st.columns([1, 2, 1])
        
        with col_center:
            if st.button("📤 Importer un Autre Fichier", width='stretch'):
                st.session_state.df = None
                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Erreur lors de la préparation du résumé: {str(e)}")


def show_report_section():
    """Affiche le rapport d'analyse complet"""
    
    df = st.session_state.df
    report_gen = ReportGenerator(df, filename="dataset")
    
    # Récupérer les informations du rapport
    summary = report_gen.get_summary_stats()
    missing_df = report_gen.get_missing_analysis()
    numeric_stats = report_gen.get_numeric_stats()
    
    # === SECTION 1: INFORMATIONS GÉNÉRALES ===
    st.markdown("### 📋 Informations Générales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Lignes", f"{summary['lignes']:,}")
    
    with col2:
        st.metric("📋 Colonnes", summary['colonnes'])
    
    with col3:
        st.metric("✨ Complétude", f"{summary['completness_pct']:.1f}%")
    
    with col4:
        st.metric("⚠️ Manquants", summary['missing_total'])
    
    # === SECTION 2: TYPES DE DONNÉES ===
    st.markdown("### 🔍 Types de Données")
    
    col_types = st.columns(len(summary['types']))
    
    for (dtype, count), col in zip(summary['types'].items(), col_types):
        with col:
            st.metric(str(dtype), count)
    
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin-top: 10px;'>
    <p><strong>📌 Types détectés:</strong> Les colonnes ont été automatiquement catégorisées selon leur type de données (numériques, texte, etc.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # === SECTION 3: ANALYSE DES VALEURS MANQUANTES ===
    st.markdown("### ⚠️ Analyse des Valeurs Manquantes")
    
    if summary['missing_total'] > 0:
        st.dataframe(
            missing_df.style.format({
                'Valeurs Manquantes': '{:d}',
                'Pourcentage': '{:.2f}%'
            }).highlight_max(subset=['Pourcentage'], color='#ffcccc'),
            width="stretch"
        )
        
        st.markdown("""
        <div style='background-color: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 10px;'>
        <p><strong>💡 Conseil:</strong> Vous pouvez utiliser l'onglet 'Nettoyage' pour traiter ces valeurs manquantes à l'aide de:</p>
        <ul>
            <li><strong>Imputation par la moyenne/médiane</strong> - pour les colonnes numériques</li>
            <li><strong>Forward Fill</strong> - pour les séries temporelles</li>
            <li><strong>Suppression des lignes</strong> - si peu de données manquantes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Excellent! Aucune valeur manquante détectée dans vos données.")
    
    st.divider()
    
    # === SECTION 4: STATISTIQUES NUMÉRIQUES ===
    if numeric_stats is not None and not numeric_stats.empty:
        st.markdown("### 📊 Statistiques Numériques Détaillées")
        
        st.dataframe(
            numeric_stats.style.format({col: '{:.2f}' for col in numeric_stats.columns if col != 'Colonne'}),
            width="stretch"
        )
        
        st.markdown("""
        <div style='background-color: #d1ecf1; padding: 15px; border-radius: 8px; margin-top: 10px;'>
        <p><strong>📌 Interprétation:</strong></p>
        <ul>
            <li><strong>Min/Max:</strong> Les valeurs minimales et maximales de chaque colonne</li>
            <li><strong>Moyenne:</strong> La valeur moyenne (sensible aux valeurs extrêmes)</li>
            <li><strong>Médiane:</strong> La valeur médiane (robuste aux valeurs extrêmes)</li>
            <li><strong>Écart-type:</strong> La variabilité des données autour de la moyenne</li>
            <li><strong>Q1/Q3:</strong> Les quartiles (25ème et 75ème percentiles)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Aucune colonne numérique trouvée dans le dataset.")


def show_report_download_section():
    """Permet de télécharger le rapport en différents formats"""
    
    df = st.session_state.df
    report_gen = ReportGenerator(df, filename="dataset")
    
    st.markdown("### 💾 Télécharger le Rapport")
    
    col1, col2, col3 = st.columns(3)
    
    # === FORMAT HTML ===
    with col1:
        st.markdown("**📄 Rapport HTML**")
        st.caption("Format web interactif")
        
        html_report = report_gen.generate_html_report()
        
        st.download_button(
            label="📥 HTML",
            data=html_report,
            file_name="rapport_analyse.html",
            mime="text/html",
            width='stretch'
        )
    
    # === FORMAT PDF ===
    with col2:
        st.markdown("**📕 Rapport PDF**")
        st.caption("Format professionnel et portable")
        
        try:
            pdf_report = report_gen.generate_pdf_report()

            if pdf_report:
                # Streamlit expects raw bytes for download; convert BytesIO to bytes
                pdf_bytes = pdf_report.getvalue() if hasattr(pdf_report, 'getvalue') else pdf_report
                st.download_button(
                    label="📥 PDF",
                    data=pdf_bytes,
                    file_name="rapport_analyse.pdf",
                    mime="application/pdf",
                    width='stretch'
                )
                # Also save a server-side copy in reports/ for reference
                try:
                    with open('reports/rapport_analyse.pdf', 'wb') as f:
                        f.write(pdf_bytes)
                except Exception as e:
                    st.warning(f"⚠️ Impossible d'enregistrer la copie serveur: {e}")
            else:
                st.warning("⚠️ PDF indisponible")
        except Exception as e:
            st.error(f"❌ Erreur PDF: {str(e)}")
    
    # === FORMAT TEXTE ===
    with col3:
        st.markdown("**📝 Rapport Texte**")
        st.caption("Format texte simple")
        
        text_report = report_gen.generate_text_report()
        
        st.download_button(
            label="📥 Texte",
            data=text_report,
            file_name="rapport_analyse.txt",
            mime="text/plain",
            width='stretch'
        )
    
    st.divider()
    
    st.markdown("""
    <div style='background-color: #e7f3ff; padding: 15px; border-radius: 8px; margin-top: 10px;'>
    <p><strong>📋 À propos du rapport:</strong></p>
    <ul>
        <li>Le rapport contient l'analyse complète de vos données</li>
        <li>Incluant: statistiques, valeurs manquantes, types de données</li>
        <li>Format PDF: idéal pour imprimer et partager</li>
        <li>Format HTML: idéal pour présenter</li>
        <li>Format Texte: parfait pour archiver</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
