"""
Traitement et analyse des données
"""
import pandas as pd
import numpy as np
from pathlib import Path


def load_file(file_path: str) -> pd.DataFrame:
    """Charger un fichier CSV ou Excel"""
    file_path = str(file_path)
    
    if file_path.endswith(('.csv', '.CSV')):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Format de fichier non supporté")


def get_data_summary(df: pd.DataFrame) -> dict:
    """Obtenir un résumé des données"""
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": df.duplicated().sum(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum() / 1024**2  # En MB
    }
    return summary


def get_column_stats(df: pd.DataFrame) -> dict:
    """Obtenir les statistiques de chaque colonne"""
    stats = {}
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            try:
                stats[col] = {
                    "type": "Quantitative",
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "mean": df[col].mean(),
                    "median": df[col].median(),
                    "std": df[col].std(),
                    "null_count": df[col].isnull().sum(),
                    "remark": None
                }
            except (ValueError, TypeError) as e:
                # If conversion failed (e.g. strings like 'Laptop' present), provide a friendly remark
                stats[col] = {
                    "type": "Quantitative",
                    "min": None,
                    "max": None,
                    "mean": None,
                    "median": None,
                    "std": None,
                    "null_count": df[col].isnull().sum(),
                    "remark": (
                        "Remarque: Cette colonne contient des valeurs non numériques (ex: 'Laptop'), "
                        "impossible de convertir toutes les valeurs en nombre. Veuillez nettoyer les valeurs "
                        "ou forcer la conversion avant d'obtenir des statistiques numériques."
                    )
                }
        else:
            stats[col] = {
                "type": "Qualitative",
                "unique_values": df[col].nunique(),
                "most_common": df[col].mode()[0] if not df[col].mode().empty else None,
                "null_count": df[col].isnull().sum()
            }
    
    return stats


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprimer les doublons"""
    initial_rows = len(df)
    df = df.drop_duplicates()
    removed_rows = initial_rows - len(df)
    return df, removed_rows


def handle_outliers(df: pd.DataFrame, column: str, method: str = "iqr") -> pd.DataFrame:
    """Gérer les valeurs aberrantes"""
    if method == "iqr":
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df


def fill_missing_values(df: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
    """Remplir les valeurs manquantes"""
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    # Pour les colonnes numériques
    if method == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif method == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif method == "forward_fill":
        df[numeric_cols] = df[numeric_cols].fillna(method='ffill')
    
    # Pour les colonnes catégorielles
    df[categorical_cols] = df[categorical_cols].fillna("Unknown")
    
    return df
