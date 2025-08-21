"""
Model service module for loan risk prediction.

This module handles model loading, feature preparation, and prediction logic.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class LoanRiskModelService:
    """Service class for loan risk prediction model operations."""
    
    def __init__(self, models_dir: Path):
        """Initialize the model service with the models directory."""
        self.models_dir = models_dir
        self.model = None
        self.scaler = None
        self.metadata = None
        self.feature_names = None
        self.is_loaded = False
        
    def load_model(self) -> None:
        """Load the trained model and associated components."""
        try:
            # Load model
            model_path = self.models_dir / "loan_risk_model.pkl"
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
            
            # Load scaler
            scaler_path = self.models_dir / "feature_scaler.pkl"
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Scaler loaded from {scaler_path}")
            
            # Load metadata
            metadata_path = self.models_dir / "model_metadata.json"
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            self.feature_names = self.metadata["feature_info"]["feature_names"]
            logger.info(f"Model metadata loaded. Features: {len(self.feature_names)}")
            
            self.is_loaded = True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise e
    
    def prepare_features(self, borrower_data: Dict[str, Any]) -> np.ndarray:
        """
        Prepare borrower features for model prediction using actual dataset column names.
        
        Args:
            borrower_data: Dictionary with borrower information using dataset column names
            
        Returns:
            Prepared feature array ready for prediction
        """
        if not self.is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
            
        try:
            # Extract basic features using actual column names
            age = borrower_data.get('Age', 35)
            income = borrower_data.get('Income', 50000)
            loan_amount = borrower_data.get('LoanAmount', 25000)
            credit_score = borrower_data.get('CreditScore', 650)
            months_employed = borrower_data.get('MonthsEmployed', 36)
            num_credit_lines = borrower_data.get('NumCreditLines', 3)
            interest_rate = borrower_data.get('InterestRate', 12.0)
            loan_term = borrower_data.get('LoanTerm', 60)
            dti_ratio = borrower_data.get('DTIRatio', 0.25)
            
            # Create feature dictionary
            features_dict = {
                'Age': age,
                'Income': income,
                'LoanAmount': loan_amount,
                'CreditScore': credit_score,
                'MonthsEmployed': months_employed,
                'NumCreditLines': num_credit_lines,
                'InterestRate': interest_rate,
                'LoanTerm': loan_term,
                'DTIRatio': dti_ratio
            }
            
            # Feature engineering (matching the notebook)
            features_dict['LoanToIncome_Ratio'] = loan_amount / (income + 1)
            
            # Monthly payment estimation
            monthly_rate = interest_rate / 100 / 12
            if monthly_rate > 0:
                features_dict['MonthlyPayment_Est'] = (
                    loan_amount * monthly_rate /
                    (1 - (1 + monthly_rate) ** (-loan_term))
                )
            else:
                features_dict['MonthlyPayment_Est'] = loan_amount / loan_term
                
            features_dict['PaymentToIncome_Ratio'] = features_dict['MonthlyPayment_Est'] / (income / 12 + 1)
            
            # Additional engineered features
            features_dict['CreditLines_Per_Year'] = num_credit_lines / max(age - 17, 1)
            features_dict['Employment_Stability'] = months_employed / max(age * 12, 1)
            
            # Risk indicators
            features_dict['HighRate_LowCredit'] = int(
                (interest_rate > 15) and (credit_score < 650)
            )
            features_dict['YoungHighDebt'] = int(
                (age < 30) and (dti_ratio > 0.3)
            )
            
            # Polynomial features
            features_dict['Age_Squared'] = age ** 2
            features_dict['Income_Log'] = np.log1p(income)
            features_dict['CreditScore_Cubed'] = credit_score ** 3
            
            # Interaction terms
            features_dict['Age_Income_Interaction'] = age * income / 1000000
            features_dict['Rate_Term_Interaction'] = interest_rate * loan_term
            
            # Categorical features (encoded)
            # Age groups
            if age <= 25:
                age_group_encoded = 0  # Young
            elif age <= 35:
                age_group_encoded = 1  # Early_Career
            elif age <= 45:
                age_group_encoded = 2  # Mid_Career
            elif age <= 55:
                age_group_encoded = 3  # Senior
            else:
                age_group_encoded = 4  # Mature
            features_dict['Age_Group_encoded'] = age_group_encoded
            
            # Income quartiles
            if income < 40000:
                income_quartile_encoded = 0  # Low
            elif income < 60000:
                income_quartile_encoded = 1  # Medium_Low
            elif income < 80000:
                income_quartile_encoded = 2  # Medium_High
            else:
                income_quartile_encoded = 3  # High
            features_dict['Income_Quartile_encoded'] = income_quartile_encoded
            
            # Loan amount quartiles
            if loan_amount < 15000:
                loan_quartile_encoded = 0  # Small
            elif loan_amount < 25000:
                loan_quartile_encoded = 1  # Medium_Small
            elif loan_amount < 35000:
                loan_quartile_encoded = 2  # Medium_Large
            else:
                loan_quartile_encoded = 3  # Large
            features_dict['LoanAmount_Quartile_encoded'] = loan_quartile_encoded
            
            # Convert to array in the correct order
            feature_array = np.array([features_dict[name] for name in self.feature_names]).reshape(1, -1)
            
            return feature_array
            
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise e
    
    def predict_risk(self, borrower_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Predict loan default risk for a borrower.
        
        Args:
            borrower_data: Dictionary with borrower information
            
        Returns:
            Tuple of (risk_score, feature_analysis)
        """
        if not self.is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
            
        try:
            # Prepare features
            feature_array = self.prepare_features(borrower_data)
            
            # Scale features
            feature_array_scaled = self.scaler.transform(feature_array)
            
            # Make prediction
            risk_score = float(self.model.predict_proba(feature_array_scaled)[0, 1])
            
            # Analyze features
            feature_analysis = self.analyze_features(borrower_data, risk_score)
            
            return risk_score, feature_analysis
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise e
    
    def analyze_features(self, borrower_data: Dict[str, Any], risk_score: float) -> Dict[str, Any]:
        """
        Analyze features and provide explanations for the prediction.
        
        Args:
            borrower_data: Dictionary with borrower information using dataset column names
            risk_score: Predicted risk score
            
        Returns:
            Dictionary with feature analysis and explanations
        """
        try:
            positive_factors = []
            negative_factors = []
            
            # Age analysis
            age = borrower_data.get('Age', 35)
            if age > 40:
                positive_factors.append("Mature age reduces default risk")
            elif age < 25:
                negative_factors.append("Young age increases default risk")
                
            # Income analysis
            income = borrower_data.get('Income', 50000)
            if income > 75000:
                positive_factors.append("High annual income")
            elif income < 40000:
                negative_factors.append("Low annual income")
                
            # Credit score analysis
            credit_score = borrower_data.get('CreditScore', 650)
            if credit_score > 750:
                positive_factors.append("Excellent credit score")
            elif credit_score > 700:
                positive_factors.append("Good credit score")
            elif credit_score < 600:
                negative_factors.append("Poor credit score")
                
            # Interest rate analysis
            interest_rate = borrower_data.get('InterestRate', 12.0)
            if interest_rate > 18:
                negative_factors.append("Very high interest rate")
            elif interest_rate > 15:
                negative_factors.append("High interest rate")
            elif interest_rate < 8:
                positive_factors.append("Low interest rate")
                
            # DTI analysis
            dti = borrower_data.get('DTIRatio', 0.25) * 100  # Convert to percentage
            if dti < 15:
                positive_factors.append("Low debt-to-income ratio")
            elif dti > 40:
                negative_factors.append("High debt-to-income ratio")
                
            # Employment analysis
            months_employed = borrower_data.get('MonthsEmployed', 36)
            employment_years = months_employed / 12
            if employment_years > 5:
                positive_factors.append("Stable employment history")
            elif employment_years < 2:
                negative_factors.append("Short employment history")
                
            # Loan amount analysis
            loan_amount = borrower_data.get('LoanAmount', 25000)
            if loan_amount > income * 0.5:
                negative_factors.append("High loan amount relative to income")
            elif loan_amount < income * 0.2:
                positive_factors.append("Conservative loan amount")
                
            return {
                "top_positive_factors": positive_factors[:3],
                "top_negative_factors": negative_factors[:3],
                "risk_score_explanation": f"Risk score of {risk_score:.1%} based on {len(positive_factors)} positive and {len(negative_factors)} negative factors",
                "feature_contributions": {
                    "age_impact": "positive" if age > 35 else "negative",
                    "income_impact": "positive" if income > 60000 else "negative",
                    "credit_impact": "positive" if credit_score > 650 else "negative",
                    "rate_impact": "negative" if interest_rate > 12 else "neutral"
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing features: {str(e)}")
            return {
                "top_positive_factors": [],
                "top_negative_factors": [],
                "risk_score_explanation": "Feature analysis unavailable",
                "feature_contributions": {}
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information and metadata."""
        if not self.is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
            
        return {
            "model_info": self.metadata["model_info"],
            "performance_metrics": self.metadata["performance_metrics"],
            "dataset_info": self.metadata["dataset_info"],
            "feature_info": self.metadata["feature_info"]
        }
    
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """Get feature importance based on correlation analysis."""
        # Based on the correlation analysis from the notebook
        return [
            {"feature": "Age", "importance": 0.168, "description": "Age of borrower"},
            {"feature": "InterestRate", "importance": 0.131, "description": "Loan interest rate"},
            {"feature": "Income", "importance": 0.099, "description": "Annual income"},
            {"feature": "MonthsEmployed", "importance": 0.097, "description": "Employment duration"},
            {"feature": "LoanAmount", "importance": 0.087, "description": "Requested loan amount"},
            {"feature": "CreditScore", "importance": 0.034, "description": "Credit score"},
            {"feature": "NumCreditLines", "importance": 0.028, "description": "Number of credit lines"},
            {"feature": "DTIRatio", "importance": 0.019, "description": "Debt-to-income ratio"},
            {"feature": "LoanTerm", "importance": 0.001, "description": "Loan term in months"}
        ]
