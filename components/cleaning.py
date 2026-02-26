"""
Page de nettoyage et analyse des données - Design Dark Blue AI
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
    """Afficher la page de nettoyage avec design Dark Blue AI"""

    # Configuration de la page
    st.set_page_config(
        page_title="DataViz AI Analytics - Analyse & Nettoyage",
        page_icon="🧹",
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

    if st.session_state.df is None:
        st.warning("Aucun fichier importé. Veuillez d'abord importer un fichier.")
        if st.button("Retour à l'importation"):
            st.session_state.current_page = "upload"
            st.rerun()
        return

    # Bouton Déconnexion en haut à droite
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Déconnexion", key="logout_cleaning"):
            st.session_state.authenticated = False
            st.session_state.current_page = "login"
            st.rerun()

    # Titre principal centré
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Analyse et Nettoyage des Données")
        st.subheader("Explorez et nettoyez vos données de manière intelligente")

    st.divider()

    # Onglets
    tabs = st.tabs(["Analyse", "Nettoyage", "Export"])

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
        st.warning("Aucun fichier importé. Veuillez d'abord importer un fichier.")
        return

    if tab_type == "analysis":
        show_analysis_tab()
    elif tab_type == "cleaning":
        show_cleaning_tab()
    elif tab_type == "export":
        show_export_tab()


def show_analysis_tab():
    """Afficher l'onglet d'analyse"""

    st.subheader("Résumé des Données")

    df = st.session_state.df

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Lignes", len(df))

    with col2:
        st.metric("Colonnes", len(df.columns))

    with col3:
        st.metric("Doublons", df.duplicated().sum())

    with col4:
        st.metric("Valeurs manquantes", df.isnull().sum().sum())

    st.divider()

    # Statistiques détaillées
    st.subheader("Statistiques par colonne")

    # Séparer colonnes numériques et catégoriques
    numeric_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(include=['object']).columns

    # Calculer statistiques détaillées via utilitaire
    stats = get_column_stats(df)
    # Convertir en DataFrame facilement
    df_stats = pd.DataFrame.from_dict(stats, orient='index')
    df_stats.index.name = 'Colonne'
    df_stats.reset_index(inplace=True)
    # renommer colonnes pour affichage
    df_stats = df_stats.rename(columns={
        'unique_values': 'Valeurs Uniques',
        'most_common': 'Plus Commun',
        'null_count': 'Manquants'
    })

    if len(numeric_cols) > 0:
        st.write("**Colonnes numériques :**")
        for col in numeric_cols[:5]:  # Limiter à 5 pour lisibilité
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"{col} - Moyenne", f"{df[col].mean():.2f}")
            with col2:
                st.metric(f"{col} - Min", f"{df[col].min():.2f}")
            with col3:
                st.metric(f"{col} - Max", f"{df[col].max():.2f}")
            with col4:
                st.metric(f"{col} - Médiane", f"{df[col].median():.2f}")

        # Boxplot avec Plotly
        st.subheader("Distribution des variables numériques")
        fig = px.box(df[numeric_cols[:5]], title="Box Plot - Distribution")
        st.plotly_chart(fig, use_container_width=True)

    if len(cat_cols) > 0:
        st.write("**Colonnes catégoriques :**")
        for col in cat_cols[:3]:  # Limiter à 3
            st.write(f"**{col}** : {df[col].nunique()} catégories uniques")
            # Diagramme en barres pour les catégories
            value_counts = df[col].value_counts().head(10)
            fig = px.bar(value_counts, title=f"Distribution de {col}")
            st.plotly_chart(fig, use_container_width=True)
    
    # afficher les stats générées précédemment
    st.dataframe(df_stats, width="stretch")
    
    st.divider()

    # Distribution des variables
    st.subheader("Distribution des Variables")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if numeric_cols:
        col_to_plot = st.selectbox("Sélectionnez une colonne", numeric_cols, key="analysis_histogram")

        fig = px.histogram(df, x=col_to_plot, nbins=30, title=f"Distribution de {col_to_plot}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune colonne numérique trouvée")

    st.divider()

    # Aperçu des premières lignes
    st.subheader("Aperçu des Données")

    n_rows = st.slider("Nombre de lignes à afficher", 1, min(50, len(df)), 10)
    st.dataframe(df.head(n_rows), use_container_width=True)

    st.divider()
    st.subheader("Télécharger le Rapport d'Analyse (PDF)")
    report_gen = ReportGenerator(df, filename="dataset_analysis")
    try:
        pdf_report = report_gen.generate_pdf_report()
        if pdf_report:
            pdf_bytes = pdf_report.getvalue() if hasattr(pdf_report, 'getvalue') else pdf_report
            st.download_button(
                label="Télécharger le rapport (PDF)",
                data=pdf_bytes,
                file_name="rapport_analyse.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            # Save server-side copy
            try:
                with open('reports/rapport_analyse_analysis.pdf', 'wb') as f:
                    f.write(pdf_bytes)
            except Exception as e:
                st.warning(f"Impossible d'enregistrer la copie serveur: {e}")
        else:
            st.warning("PDF indisponible")
    except Exception as e:
        st.error(f"Erreur génération PDF: {str(e)}")


def show_cleaning_tab():
    """Afficher l'onglet de nettoyage"""

    st.subheader("Actions de Nettoyage")

    df = st.session_state.df
    original_len = len(df)

    # Compteur avant/après nettoyage
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Lignes avant nettoyage", original_len)
    with col2:
        st.metric("Lignes actuelles", len(df))

    st.divider()

    # === SUPPRESSION DES DOUBLONS ===
    with st.container():
        st.subheader("Supprimer les Doublons")

        col1, col2 = st.columns([3, 1])

        with col1:
            duplicates_count = df.duplicated().sum()
            if duplicates_count > 0:
                st.warning(f"{duplicates_count} doublons détectés dans vos données")
            else:
                st.success("Aucun doublon détecté")

        with col2:
            if st.button("Supprimer les doublons", use_container_width=True):
                if duplicates_count > 0:
                    df_cleaned, removed_rows = remove_duplicates(df)
                    st.session_state.df = df_cleaned
                    st.success(f"{removed_rows} doublons supprimés")
                    st.rerun()

    st.divider()

    # === VALEURS MANQUANTES ===
    with st.container():
        st.subheader("Traiter les Valeurs Manquantes")

        missing_total = df.isnull().sum().sum()

        if missing_total > 0:
            st.warning(f"{int(missing_total)} valeurs manquantes détectées")

            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                method = st.selectbox(
                    "Sélectionnez la méthode de traitement",
                    ["mean", "median", "forward_fill"],
                    format_func=lambda x: {
                        "mean": "Moyenne",
                        "median": "Médiane",
                        "forward_fill": "Forward Fill"
                    }[x],
                    key="fill_method"
                )

            with col3:
                if st.button("Remplir", use_container_width=True):
                    df_filled = fill_missing_values(st.session_state.df, method=method)
                    st.session_state.df = df_filled
                    st.success(f"Valeurs manquantes traitées avec: {method}")
                    st.rerun()
        else:
            st.success("Aucune valeur manquante détectée")

    st.divider()

    # === VALEURS ABERRANTES ===
    with st.container():
        st.subheader("Gérer les Valeurs Aberrantes (Outliers)")

        numeric_cols = st.session_state.df.select_dtypes(include=['number']).columns.tolist()

        if numeric_cols:
            col_to_clean = st.selectbox(
                "Sélectionnez une colonne numérique à analyser",
                numeric_cols,
                key="outlier_col"
            )

            col1, col2 = st.columns([2, 1])

            with col1:
                # Boxplot avec Plotly
                fig = px.box(
                    st.session_state.df,
                    y=col_to_clean,
                    title=f"Distribution - {col_to_clean}",
                    color_discrete_sequence=["#2563EB"]
                )
                fig.update_layout(
                    height=400,
                    template="plotly_white",
                    font=dict(size=12)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                outliers_stats = st.session_state.df[col_to_clean].describe()
                st.metric("Min", f"{outliers_stats['min']:.2f}")
                st.metric("Q1", f"{st.session_state.df[col_to_clean].quantile(0.25):.2f}")
                st.metric("Médiane", f"{outliers_stats['50%']:.2f}")
                st.metric("Q3", f"{st.session_state.df[col_to_clean].quantile(0.75):.2f}")
                st.metric("Max", f"{outliers_stats['max']:.2f}")

                if st.button("Supprimer Outliers", use_container_width=True):
                    df_cleaned = handle_outliers(st.session_state.df, col_to_clean)
                    rows_removed = len(st.session_state.df) - len(df_cleaned)
                    st.session_state.df = df_cleaned
                    st.success(f"{rows_removed} valeurs aberrantes supprimées")
                    st.rerun()
        else:
            st.info("Aucune colonne numérique trouvée pour l'analyse des outliers")

    st.divider()

    # === RÉSUMÉ APRÈS NETTOYAGE ===
    with st.container():
        st.subheader("Résumé Après Nettoyage")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Lignes", len(st.session_state.df))

        with col2:
            st.metric("Colonnes", len(st.session_state.df.columns))

        with col3:
            st.metric("Doublons", st.session_state.df.duplicated().sum())

        with col4:
            st.metric("Valeurs manquantes", st.session_state.df.isnull().sum().sum())

    st.divider()

    # === TÉLÉCHARGER LES DONNÉES NETTOYÉES ===
    with st.container():
        st.subheader("Télécharger les Données Nettoyées")

        try:
            df = st.session_state.df

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Format CSV**")
                csv_data = DataExporter.to_csv(df)
                if csv_data:
                    st.download_button(
                        label="Télécharger en CSV",
                        data=csv_data,
                        file_name="donnees_nettoyees.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

            with col2:
                st.markdown("**Format Excel**")
                excel_buffer = DataExporter.to_excel(df)
                if excel_buffer:
                    st.download_button(
                        label="Télécharger en Excel",
                        data=excel_buffer,
                        file_name="donnees_nettoyees.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"Erreur lors de l'export: {str(e)}")


def show_export_tab():
    """Afficher l'onglet d'export avec rapport professionnel"""

    df = st.session_state.df

    if df is None or df.empty:
        st.warning("Aucune donnée à exporter. Veuillez d'abord importer un fichier.")
        return

    # ========== SECTION 1: RAPPORT D'ANALYSE ==========
    st.subheader("Rapport d'Analyse Après Nettoyage")

    # Onglets pour rapport
    tab_report, tab_download = st.tabs(["Rapport", "Télécharger Rapport"])

    with tab_report:
        try:
            show_report_section()
        except Exception as e:
            st.error(f"Erreur lors de la génération du rapport: {str(e)}")

    with tab_download:
        try:
            show_report_download_section()
        except Exception as e:
            st.error(f"Erreur lors de la préparation du téléchargement: {str(e)}")

    st.divider()

    # ========== SECTION 2: EXPORT DES DONNÉES NETTOYÉES ==========
    st.subheader("Télécharger les Données Nettoyées")

    try:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Format CSV")
            csv_data = DataExporter.to_csv(df)
            if csv_data:
                st.download_button(
                    label="Télécharger en CSV",
                    data=csv_data,
                    file_name="donnees_nettoyees.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            st.caption("Format standard pour Excel, Google Sheets, etc.")

        with col2:
            st.markdown("### Format Excel")
            excel_buffer = DataExporter.to_excel(df)
            if excel_buffer:
                st.download_button(
                    label="Télécharger en Excel",
                    data=excel_buffer,
                    file_name="donnees_nettoyees.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            st.caption("Format Excel avec feuille 'Résumé' des statistiques")
    except Exception as e:
        st.error(f"Erreur lors de l'export des données: {str(e)}")

    st.divider()

    # ========== SECTION 3: RÉSUMÉ FINAL ==========
    st.subheader("Résumé du Nettoyage")

    try:
        info_export = DataExporter.get_export_info(df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Lignes", f"{info_export['lignes']:,}")

        with col2:
            st.metric("Colonnes", info_export['colonnes'])

        with col3:
            st.metric("Qualité", f"{info_export['completness_pct']:.1f}%")

        with col4:
            st.metric("Manquants", info_export['missing_total'])

        st.info(f"""
        **Données nettoyées et prêtes à l'emploi!**

        Votre dataset contient maintenant **{info_export['lignes']:,} lignes** et **{info_export['colonnes']} colonnes**

        Complétude des données: **{info_export['completness_pct']:.1f}%**

        Vous pouvez maintenant:
        - Télécharger les données nettoyées en CSV ou Excel
        - Utiliser les données pour la visualisation
        - Entraîner des modèles de machine learning
        """)

        st.divider()

        # Navigation
        col_left, col_center, col_right = st.columns([1, 2, 1])

        with col_center:
            if st.button("Importer un Autre Fichier", use_container_width=True):
                st.session_state.df = None
                st.rerun()

    except Exception as e:
        st.error(f"Erreur lors de la préparation du résumé: {str(e)}")


def show_report_section():
    """Affiche le rapport d'analyse complet"""

    df = st.session_state.df
    report_gen = ReportGenerator(df, filename="dataset")

    # Récupérer les informations du rapport
    summary = report_gen.get_summary_stats()
    missing_df = report_gen.get_missing_analysis()
    numeric_stats = report_gen.get_numeric_stats()

    # === SECTION 1: INFORMATIONS GÉNÉRALES ===
    st.subheader("Informations Générales")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Lignes", f"{summary['lignes']:,}")

    with col2:
        st.metric("Colonnes", summary['colonnes'])

    with col3:
        st.metric("Complétude", f"{summary['completness_pct']:.1f}%")

    with col4:
        st.metric("Manquants", summary['missing_total'])

    # === SECTION 2: TYPES DE DONNÉES ===
    st.subheader("Types de Données")

    col_types = st.columns(len(summary['types']))

    for (dtype, count), col in zip(summary['types'].items(), col_types):
        with col:
            st.metric(str(dtype), count)

    st.info("Types détectés: Les colonnes ont été automatiquement catégorisées selon leur type de données (numériques, texte, etc.)")

    st.divider()

    # === SECTION 3: ANALYSE DES VALEURS MANQUANTES ===
    st.subheader("Analyse des Valeurs Manquantes")

    if summary['missing_total'] > 0:
        st.dataframe(
            missing_df.style.format({
                'Valeurs Manquantes': '{:d}',
                'Pourcentage': '{:.2f}%'
            }).highlight_max(subset=['Pourcentage'], color='#ffcccc'),
            use_container_width=True
        )

        st.info("""
        **Conseil:** Vous pouvez utiliser l'onglet 'Nettoyage' pour traiter ces valeurs manquantes à l'aide de:

        • Imputation par la moyenne/médiane - pour les colonnes numériques
        • Forward Fill - pour les séries temporelles
        • Suppression des lignes - si peu de données manquantes
        """)
    else:
        st.success("Excellent! Aucune valeur manquante détectée dans vos données.")

    st.divider()

    # === SECTION 4: STATISTIQUES NUMÉRIQUES ===
    if numeric_stats is not None and not numeric_stats.empty:
        st.subheader("Statistiques Numériques Détaillées")

        st.dataframe(
            numeric_stats.style.format({col: '{:.2f}' for col in numeric_stats.columns if col != 'Colonne'}),
            use_container_width=True
        )

        st.info("""
        **Interprétation:**

        • Min/Max: Les valeurs minimales et maximales de chaque colonne
        • Moyenne: La valeur moyenne (sensible aux valeurs extrêmes)
        • Médiane: La valeur médiane (robuste aux valeurs extrêmes)
        • Écart-type: La variabilité des données autour de la moyenne
        • Q1/Q3: Les quartiles (25ème et 75ème percentiles)
        """)
    else:
        st.info("Aucune colonne numérique trouvée dans le dataset.")


def show_report_download_section():
    """Permet de télécharger le rapport en différents formats"""

    df = st.session_state.df
    report_gen = ReportGenerator(df, filename="dataset")

    st.subheader("Télécharger le Rapport")

    col1, col2, col3 = st.columns(3)

    # === FORMAT HTML ===
    with col1:
        st.markdown("**Rapport HTML**")
        st.caption("Format web interactif")

        html_report = report_gen.generate_html_report()

        st.download_button(
            label="HTML",
            data=html_report,
            file_name="rapport_analyse.html",
            mime="text/html",
            use_container_width=True
        )

    # === FORMAT PDF ===
    with col2:
        st.markdown("**Rapport PDF**")
        st.caption("Format professionnel et portable")

        try:
            pdf_report = report_gen.generate_pdf_report()

            if pdf_report:
                # Streamlit expects raw bytes for download; convert BytesIO to bytes
                pdf_bytes = pdf_report.getvalue() if hasattr(pdf_report, 'getvalue') else pdf_report
                st.download_button(
                    label="PDF",
                    data=pdf_bytes,
                    file_name="rapport_analyse.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                # Also save a server-side copy in reports/ for reference
                try:
                    with open('reports/rapport_analyse.pdf', 'wb') as f:
                        f.write(pdf_bytes)
                except Exception as e:
                    st.warning(f"Impossible d'enregistrer la copie serveur: {e}")
            else:
                st.warning("PDF indisponible")
        except Exception as e:
            st.error(f"Erreur PDF: {str(e)}")

    # === FORMAT TEXTE ===
    with col3:
        st.markdown("**Rapport Texte**")
        st.caption("Format texte simple")

        text_report = report_gen.generate_text_report()

        st.download_button(
            label="Texte",
            data=text_report,
            file_name="rapport_analyse.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()

    st.info("""
    **À propos du rapport:**

    • Le rapport contient l'analyse complète de vos données
    • Incluant: statistiques, valeurs manquantes, types de données
    • Format PDF: idéal pour imprimer et partager
    • Format HTML: idéal pour présenter
    • Format Texte: parfait pour archiver
    """)
