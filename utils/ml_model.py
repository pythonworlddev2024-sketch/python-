"""
Modèles de prédiction et analyse
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score


class PredictionModel:
    """Classe pour gérer les modèles de prédiction"""
    
    def __init__(self, df: pd.DataFrame, target_column: str):
        self.df = df.copy()
        self.target_column = target_column
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_classification = False
        self._prepare_data()
    
    def _prepare_data(self):
        """Préparer les données pour l'entraînement"""
        # Déterminer si c'est un problème de classification ou régression
        unique_values = self.df[self.target_column].nunique()
        self.is_classification = unique_values < 20 or self.df[self.target_column].dtype == 'object'
        
        # Séparer features et target
        self.X = self.df.drop(columns=[self.target_column])
        self.y = self.df[self.target_column]
        
        # Robust encoding for non-numeric columns and safe numeric conversion
        for col in self.X.columns:
            # Coerce numeric-like columns to numeric (non-convertible -> NaN)
            if pd.api.types.is_numeric_dtype(self.X[col]):
                self.X[col] = pd.to_numeric(self.X[col], errors='coerce')
            else:
                # For categorical/string-like columns, use LabelEncoder after filling NaN
                try:
                    le = LabelEncoder()
                    filled = self.X[col].fillna('__MISSING__').astype(str)
                    self.X[col] = le.fit_transform(filled)
                    self.label_encoders[col] = le
                except Exception:
                    # Fallback: convert to string values then to codes
                    self.X[col] = self.X[col].fillna('__MISSING__').astype(str).apply(lambda x: hash(x) % 1000000)

            # Booleans -> int
            if self.X[col].dtype == 'bool':
                self.X[col] = self.X[col].astype(int)

        # Encoder la variable cible si classification
        if self.is_classification:
            if self.y.dtype == 'object' or not pd.api.types.is_numeric_dtype(self.y):
                le = LabelEncoder()
                self.y = le.fit_transform(self.y.fillna('__MISSING__').astype(str))
                self.label_encoders['target'] = le
            else:
                # coerce numeric target
                self.y = pd.to_numeric(self.y, errors='coerce')

        # Pour les colonnes numériques restantes: remplir NaN par la moyenne
        for col in self.X.columns:
            if pd.api.types.is_numeric_dtype(self.X[col]):
                if self.X[col].isnull().any():
                    try:
                        self.X[col] = self.X[col].fillna(self.X[col].mean())
                    except Exception:
                        self.X[col] = self.X[col].fillna(0)

        # Final check: ensure all values are numeric for scaler
        try:
            numeric_X = self.X.select_dtypes(include=[np.number])
            # If there are non-numeric columns left, coerce them
            if numeric_X.shape[1] != self.X.shape[1]:
                for col in self.X.columns:
                    if not pd.api.types.is_numeric_dtype(self.X[col]):
                        self.X[col] = pd.to_numeric(self.X[col], errors='coerce').fillna(0)

            self.X = pd.DataFrame(
                self.scaler.fit_transform(self.X),
                columns=self.X.columns
            )
        except Exception as e:
            raise ValueError(f"Erreur lors de la préparation des données pour le modèle: {e}")
    
    def train(self):
        """Entraîner le modèle"""
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        if self.is_classification:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
        else:
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train, y_train)
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
        
        return {"train_score": train_score, "test_score": test_score}
    
    def predict(self, input_data: dict):
        """Faire une prédiction"""
        if self.model is None:
            self.train()
        
        # Préparer l'entrée
        df_input = pd.DataFrame([input_data])
        
        for col in df_input.columns:
            if col in self.label_encoders:
                try:
                    df_input[col] = self.label_encoders[col].transform(df_input[col])
                except:
                    df_input[col] = 0
        
        # Normaliser
        df_input = pd.DataFrame(
            self.scaler.transform(df_input),
            columns=df_input.columns
        )
        
        # Prédire
        prediction = self.model.predict(df_input)[0]
        
        if self.is_classification and 'target' in self.label_encoders:
            prediction = self.label_encoders['target'].inverse_transform([int(prediction)])[0]
        
        return prediction
    
    def get_feature_importance(self):
        """Obtenir l'importance des features"""
        if self.model is None:
            self.train()
        
        importances = self.model.feature_importances_
        feature_names = self.X.columns
        
        return dict(zip(feature_names, importances))
