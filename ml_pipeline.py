# ==================================================
# ML PIPELINE & MODEL MANAGEMENT
# ==================================================

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path
from config import MODEL_PATH, MODEL_ENCODER_PATH, CSV_DATA_PATH
import streamlit as st


class MLPipeline:
    """Machine Learning Pipeline for Churn Prediction"""

    def __init__(self):
        self.model = None
        self.encoders = {}
        self.feature_columns = None
        self.accuracy = None
        self.load_or_train_model()

    def load_or_train_model(self):
        """Load existing model or train new one"""
        model_path = Path(MODEL_PATH)
        encoder_path = Path(MODEL_ENCODER_PATH)

        if model_path.exists() and encoder_path.exists():
            # Load existing model
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            with open(MODEL_ENCODER_PATH, "rb") as f:
                self.encoders = pickle.load(f)
        else:
            # Train new model
            self.train_model()

    def train_model(self):
        """Train Random Forest model on CSV data"""
        try:
            # Load data
            df = pd.read_csv(CSV_DATA_PATH)
            data = df.copy()

            # Drop non-predictive columns
            data = data.drop(["CustomerId", "Surname"], axis=1, errors="ignore")

            # Encode categorical variables
            for col in data.select_dtypes(include="object").columns:
                encoder = LabelEncoder()
                data[col] = encoder.fit_transform(data[col])
                self.encoders[col] = encoder

            # Store feature columns
            self.feature_columns = [col for col in data.columns if col != "Exited"]

            # Split data
            X = data[self.feature_columns]
            y = data["Exited"]
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            self.model.fit(X_train, y_train)

            # Calculate accuracy
            predictions = self.model.predict(X_test)
            self.accuracy = accuracy_score(y_test, predictions)

            # Save model
            Path(MODEL_PATH).parent.mkdir(parents=True, exist_ok=True)
            with open(MODEL_PATH, "wb") as f:
                pickle.dump(self.model, f)
            with open(MODEL_ENCODER_PATH, "wb") as f:
                pickle.dump(self.encoders, f)

        except Exception as e:
            print(f"Error training model: {e}")

    def predict_churn(
        self, customer_data: dict, customer_id: str = None
    ) -> dict:
        """Predict churn probability for customer"""
        try:
            # Prepare data
            data = pd.DataFrame([customer_data])

            # Drop non-predictive columns
            data = data.drop(
                ["customer_id", "first_name", "last_name", "email", "phone",
                 "date_of_birth", "occupation", "annual_income", "estimated_salary",
                 "risk_preference", "account_type", "branch", "manager", "notes",
                 "status", "created_at", "updated_at", "created_by"],
                axis=1, errors="ignore"
            )

            # Encode categorical variables
            for col in data.select_dtypes(include="object").columns:
                if col in self.encoders:
                    data[col] = self.encoders[col].transform(data[col])
                else:
                    data[col] = 0

            # Select only feature columns
            data = data[self.feature_columns]

            # Predict
            probability = self.model.predict_proba(data)[0][1]
            prediction = self.model.predict(data)[0]

            # Calculate engagement score
            engagement_score = self.calculate_engagement_score(customer_data)

            # Determine risk level
            if probability > 0.7:
                risk_level = "Critical"
            elif probability > 0.5:
                risk_level = "High"
            elif probability > 0.3:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            return {
                "engagement_score": engagement_score,
                "churn_probability": probability * 100,
                "risk_level": risk_level,
                "is_churned": int(prediction),
                "model_version": "1.0",
            }
        except Exception as e:
            print(f"Error predicting churn: {e}")
            return None

    def calculate_engagement_score(self, customer_data: dict) -> float:
        """Calculate engagement score for customer"""
        try:
            balance = float(customer_data.get("balance", 0))
            num_products = int(customer_data.get("num_of_products", 0))
            is_active = int(customer_data.get("is_active_member", 0))

            # Normalize scores
            balance_score = min((balance / 250000) * 40, 40)  # Max 40
            product_score = min((num_products / 4) * 30, 30)  # Max 30
            activity_score = is_active * 30  # Max 30

            total_score = balance_score + product_score + activity_score
            return round(total_score, 2)
        except Exception:
            return 0.0

    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance ranking"""
        if self.model is None:
            return None

        importance = pd.DataFrame(
            {
                "Feature": self.feature_columns,
                "Importance": self.model.feature_importances_,
            }
        ).sort_values("Importance", ascending=False)

        return importance

    def get_model_accuracy(self) -> float:
        """Get model accuracy"""
        return self.accuracy if self.accuracy else 0.0
