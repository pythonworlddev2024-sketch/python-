"""
Générateur de rapports professionnels pour l'analyse de données nettoyées
Support: HTML et texte structuré
"""

import pandas as pd
import numpy as np
from datetime import datetime
from io import StringIO, BytesIO


class ReportGenerator:
    """Génère des rapports d'analyse professionnels"""
    
    def __init__(self, df, filename="data"):
        """
        Initialise le générateur de rapport
        
        Args:
            df: DataFrame pandas
            filename: nom du fichier source
        """
        self.df = df
        self.filename = filename
        self.timestamp = datetime.now()
    
    def get_summary_stats(self):
        """Récupère les statistiques résumées"""
        return {
            'lignes': len(self.df),
            'colonnes': len(self.df.columns),
            'types': self.df.dtypes.value_counts().to_dict(),
            'missing_total': int(self.df.isnull().sum().sum()),
            'missing_pct': (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100,
            'doublons': int(self.df.duplicated().sum()),
            'completness_pct': 100 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        }
    
    def get_missing_analysis(self):
        """Analyse détaillée des valeurs manquantes par colonne"""
        missing_info = []
        
        for col in self.df.columns:
            nan_count = int(self.df[col].isnull().sum())
            nan_pct = (nan_count / len(self.df)) * 100
            
            missing_info.append({
                'Colonne': col,
                'Valeurs Manquantes': nan_count,
                'Pourcentage': nan_pct
            })
        
        return pd.DataFrame(missing_info)
    
    def get_numeric_stats(self):
        """Statistiques numériques pour les colonnes quantitatives"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return None
        
        stats = []
        for col in numeric_df.columns:
            col_data = numeric_df[col]
            
            stats.append({
                'Colonne': col,
                'Min': f"{col_data.min():.2f}",
                'Max': f"{col_data.max():.2f}",
                'Moyenne': f"{col_data.mean():.2f}",
                'Médiane': f"{col_data.median():.2f}",
                'Écart-type': f"{col_data.std():.2f}",
                'Q1': f"{col_data.quantile(0.25):.2f}",
                'Q3': f"{col_data.quantile(0.75):.2f}"
            })
        
        return pd.DataFrame(stats)
    
    def generate_html_report(self):
        """Génère un rapport HTML professionnel"""
        
        summary = self.get_summary_stats()
        missing_df = self.get_missing_analysis()
        numeric_stats = self.get_numeric_stats()
        
        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Analyse - {self.filename}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background-color: #ecf0f1;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }}
        
        .header {{
            border-bottom: 4px solid #3498db;
            margin-bottom: 30px;
            padding-bottom: 20px;
        }}
        
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            font-size: 12px;
            color: #7f8c8d;
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: bold;
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-bottom: 15px;
            margin-top: 25px;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .metric-box {{
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            border-radius: 4px;
        }}
        
        .metric-box.warning {{
            border-left-color: #f39c12;
        }}
        
        .metric-box.danger {{
            border-left-color: #e74c3c;
        }}
        
        .metric-box.success {{
            border-left-color: #2ecc71;
        }}
        
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
            text-transform: uppercase;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        table thead {{
            background-color: #34495e;
            color: white;
        }}
        
        table th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        table tbody tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .description {{
            background-color: #ecf0f1;
            border-left: 4px solid #3498db;
            padding: 15px;
            border-radius: 4px;
            margin-top: 15px;
            font-size: 14px;
            color: #555;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            font-size: 12px;
            color: #7f8c8d;
        }}
        
        .high-quality {{
            color: #2ecc71;
            font-weight: bold;
        }}
        
        .medium-quality {{
            color: #f39c12;
            font-weight: bold;
        }}
        
        .low-quality {{
            color: #e74c3c;
            font-weight: bold;
        }}
        
        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- EN-TÊTE -->
        <div class="header">
            <h1>📊 Rapport d'Analyse de Données</h1>
            <div class="meta">
                <p><strong>Fichier:</strong> {self.filename}</p>
                <p><strong>Date:</strong> {self.timestamp.strftime('%d/%m/%Y à %H:%M:%S')}</p>
            </div>
        </div>
        
        <!-- SECTION 1: INFORMATIONS GÉNÉRALES -->
        <div class="section">
            <div class="section-title">📋 Informations Générales</div>
            
            <div class="metrics">
                <div class="metric-box">
                    <div class="metric-label">Nombre de Lignes</div>
                    <div class="metric-value">{summary['lignes']:,}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Nombre de Colonnes</div>
                    <div class="metric-value">{summary['colonnes']}</div>
                </div>
                <div class="metric-box success">
                    <div class="metric-label">Complétude</div>
                    <div class="metric-value">{summary['completness_pct']:.1f}%</div>
                </div>
                <div class="metric-box warning">
                    <div class="metric-label">Valeurs Manquantes</div>
                    <div class="metric-value">{summary['missing_total']}</div>
                </div>
            </div>
            
            <div class="description">
                <strong>📌 Résumé:</strong> Votre dataset contient <strong>{summary['lignes']:,} lignes</strong> et 
                <strong>{summary['colonnes']} colonnes</strong>. La qualité des données est de 
                <span class="{'high-quality' if summary['completness_pct'] >= 95 else 'medium-quality' if summary['completness_pct'] >= 80 else 'low-quality'}">
                {summary['completness_pct']:.1f}%
                </span>.
            </div>
        </div>
        
        <!-- SECTION 2: TYPES DE DONNÉES -->
        <div class="section">
            <div class="section-title">🔍 Types de Données</div>
            <div style="margin-top: 15px;">
"""
        
        # Ajouter les types de données
        for dtype, count in summary['types'].items():
            html += f"<p><strong>{str(dtype)}:</strong> {count} colonne(s)</p>"
        
        html += """
            </div>
        </div>
        
        <!-- SECTION 3: ANALYSE DES VALEURS MANQUANTES -->
        <div class="section">
            <div class="section-title">⚠️ Analyse des Valeurs Manquantes</div>
"""
        
        if summary['missing_total'] > 0:
            html += missing_df.to_html(index=False, border=0)
            html += f"""
            <div class="description" style="margin-top: 15px;">
                <strong>💡 Conseil:</strong> {summary['missing_total']} valeur(s) manquante(s) détectée(s). 
                Vous pouvez utiliser l'onglet Nettoyage pour les traiter via imputation (moyenne, médiane, forward-fill).
            </div>
"""
        else:
            html += """
            <div class="description" style="margin-top: 15px; border-left-color: #2ecc71; background-color: #d5f4e6;">
                <strong>✅ Excellent:</strong> Aucune valeur manquante détectée dans vos données!
            </div>
"""
        
        html += """
        </div>
        
        <!-- SECTION 4: STATISTIQUES NUMÉRIQUES -->
        <div class="section">
            <div class="section-title">📊 Statistiques Numériques</div>
"""
        
        if numeric_stats is not None and not numeric_stats.empty:
            html += numeric_stats.to_html(index=False, border=0)
        else:
            html += "<p><em>Aucune colonne numérique trouvée dans le dataset.</em></p>"
        
        html += """
        </div>
        
        <!-- PIED DE PAGE -->
        <div class="footer">
            <p>Rapport généré automatiquement par <strong>DataViz AI Analytics</strong> © 2025</p>
            <p>Pour plus d'informations, consultez l'onglet Analyse dans l'application.</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_text_report(self):
        """Génère un rapport en format texte simple"""
        
        summary = self.get_summary_stats()
        missing_df = self.get_missing_analysis()
        numeric_stats = self.get_numeric_stats()
        
        report = StringIO()
        
        report.write("=" * 80 + "\n")
        report.write("RAPPORT D'ANALYSE DE DONNÉES\n")
        report.write("=" * 80 + "\n\n")
        
        report.write(f"Fichier: {self.filename}\n")
        report.write(f"Date: {self.timestamp.strftime('%d/%m/%Y à %H:%M:%S')}\n\n")
        
        # Section informations générales
        report.write("-" * 80 + "\n")
        report.write("INFORMATIONS GÉNÉRALES\n")
        report.write("-" * 80 + "\n")
        report.write(f"Nombre de lignes: {summary['lignes']:,}\n")
        report.write(f"Nombre de colonnes: {summary['colonnes']}\n")
        report.write(f"Valeurs manquantes (total): {summary['missing_total']} ({summary['missing_pct']:.2f}%)\n")
        report.write(f"Complétude des données: {summary['completness_pct']:.2f}%\n")
        report.write(f"Doublons détectés: {summary['doublons']}\n\n")
        
        # Section types de données
        report.write("-" * 80 + "\n")
        report.write("TYPES DE DONNÉES\n")
        report.write("-" * 80 + "\n")
        for dtype, count in summary['types'].items():
            report.write(f"{str(dtype)}: {count} colonne(s)\n")
        report.write("\n")
        
        # Section valeurs manquantes détaillées
        report.write("-" * 80 + "\n")
        report.write("ANALYSE DES VALEURS MANQUANTES PAR COLONNE\n")
        report.write("-" * 80 + "\n")
        report.write(missing_df.to_string(index=False))
        report.write("\n\n")
        
        # Section statistiques numériques
        if numeric_stats is not None and not numeric_stats.empty:
            report.write("-" * 80 + "\n")
            report.write("STATISTIQUES NUMÉRIQUES\n")
            report.write("-" * 80 + "\n")
            report.write(numeric_stats.to_string(index=False))
            report.write("\n\n")
        
        report.write("=" * 80 + "\n")
        report.write("FIN DU RAPPORT\n")
        report.write("=" * 80 + "\n")
        
        return report.getvalue()
    
    def generate_pdf_report(self):
        """Génère un rapport PDF professionnel avec reportlab"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
        except ImportError:
            return None
        
        summary = self.get_summary_stats()
        missing_df = self.get_missing_analysis()
        numeric_stats = self.get_numeric_stats()
        
        # Créer un BytesIO pour le PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=1
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        elements = []
        
        # Titre
        elements.append(Paragraph("📊 Rapport d'Analyse de Données", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Métadonnées
        meta_text = f"<b>Fichier:</b> {self.filename} | <b>Date:</b> {self.timestamp.strftime('%d/%m/%Y à %H:%M')}"
        elements.append(Paragraph(meta_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Section 1: Informations générales
        elements.append(Paragraph("1. Informations Générales", heading_style))
        
        summary_data = [
            ['Métrique', 'Valeur'],
            ['Nombre de lignes', f"{summary['lignes']:,}"],
            ['Nombre de colonnes', f"{summary['colonnes']}"],
            ['Valeurs manquantes', f"{summary['missing_total']} ({summary['missing_pct']:.2f}%)"],
            ['Complétude', f"{summary['completness_pct']:.2f}%"],
            ['Doublons', f"{summary['doublons']}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Section 2: Types de données
        elements.append(Paragraph("2. Types de Données", heading_style))
        types_text = ", ".join([f"<b>{str(dtype)}</b>: {count} col(s)" for dtype, count in summary['types'].items()])
        elements.append(Paragraph(types_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Section 3: Valeurs manquantes
        elements.append(Paragraph("3. Analyse des Valeurs Manquantes", heading_style))
        
        if summary['missing_total'] > 0:
            missing_data = [['Colonne', 'Manquantes', 'Pourcentage']]
            for _, row in missing_df.iterrows():
                missing_data.append([
                    row['Colonne'],
                    str(row['Valeurs Manquantes']),
                    f"{row['Pourcentage']:.2f}%"
                ])
            
            missing_table = Table(missing_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            missing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(missing_table)
        else:
            elements.append(Paragraph("✅ Aucune valeur manquante", styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Section 4: Statistiques numériques
        if numeric_stats is not None and not numeric_stats.empty:
            elements.append(PageBreak())
            elements.append(Paragraph("4. Statistiques Numériques Détaillées", heading_style))
            
            numeric_data = [['Colonne', 'Min', 'Max', 'Moyenne', 'Médiane', 'Écart-type']]
            for _, row in numeric_stats.iterrows():
                numeric_data.append([
                    row['Colonne'],
                    row['Min'],
                    row['Max'],
                    row['Moyenne'],
                    row['Médiane'],
                    row['Écart-type']
                ])
            
            numeric_table = Table(numeric_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch])
            numeric_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(numeric_table)

        # Section 5: Corrélations (si applicable)
        try:
            numeric_df = self.df.select_dtypes(include=[np.number])
            if numeric_df.shape[1] >= 2:
                elements.append(PageBreak())
                elements.append(Paragraph("5. Matrice de Corrélations (numériques)", heading_style))
                corr = numeric_df.corr().round(3)
                # Build table header
                corr_data = [ [""] + corr.columns.tolist() ]
                for idx in corr.index:
                    row = [str(idx)] + [str(corr.loc[idx, c]) for c in corr.columns]
                    corr_data.append(row)

                corr_table = Table(corr_data, colWidths=[1.2*inch] + [0.7*inch]*len(corr.columns))
                corr_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
                ]))
                elements.append(corr_table)
                elements.append(Spacer(1, 0.3*inch))
        except Exception:
            pass

        # Section 6: Aperçu des premières lignes
        try:
            elements.append(PageBreak())
            elements.append(Paragraph("6. Aperçu (5 premières lignes)", heading_style))
            sample_df = self.df.head(5).astype(str)
            sample_data = [sample_df.columns.tolist()]
            for _, r in sample_df.iterrows():
                sample_data.append(list(r.values))

            sample_table = Table(sample_data, colWidths=[1*inch]*len(sample_df.columns))
            sample_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(sample_table)
            elements.append(Spacer(1, 0.3*inch))
        except Exception:
            pass
        
        # Pied de page
        elements.append(Spacer(1, 0.5*inch))
        footer_text = "Rapport généré automatiquement par <b>DataViz AI Analytics</b> © 2025"
        elements.append(Paragraph(footer_text, styles['Normal']))
        
        # Construire le PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        
        return pdf_buffer
