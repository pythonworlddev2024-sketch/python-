"""
Fonctions d'export de données nettoyées
Support: CSV, Excel
"""

import pandas as pd
from io import BytesIO


class DataExporter:
    """Exporte les données dans différents formats"""
    
    @staticmethod
    def to_csv(df, filename="donnees_nettoyees"):
        """
        Exporte les données en CSV
        
        Args:
            df: DataFrame pandas
            filename: nom du fichier (sans extension)
            
        Returns:
            bytes: données CSV compressées
        """
        csv_data = df.to_csv(index=False)
        return csv_data
    
    @staticmethod
    def to_excel(df, filename="donnees_nettoyees"):
        """
        Exporte les données en Excel (.xlsx)
        
        Args:
            df: DataFrame pandas
            filename: nom du fichier (sans extension)
            
        Returns:
            BytesIO: fichier Excel en mémoire
        """
        excel_buffer = BytesIO()
        
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Données')
            
            # Ajouter des meta-informations
            summary_data = {
                'Métrique': [
                    'Nombre de lignes',
                    'Nombre de colonnes',
                    'Valeurs manquantes',
                    'Complétude (%)'
                ],
                'Valeur': [
                    len(df),
                    len(df.columns),
                    int(df.isnull().sum().sum()),
                    round(100 - (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2)
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, index=False, sheet_name='Résumé')
        
        excel_buffer.seek(0)
        return excel_buffer
    
    @staticmethod
    def get_export_info(df):
        """
        Récupère les informations de la base nettoyée
        
        Returns:
            dict: informations sur les données
        """
        return {
            'lignes': len(df),
            'colonnes': len(df.columns),
            'colonnes_list': df.columns.tolist(),
            'types': df.dtypes.to_dict(),
            'missing_total': int(df.isnull().sum().sum()),
            'missing_pct': round((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
            'doublons': int(df.duplicated().sum()),
            'completness_pct': round(100 - (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2)
        }
