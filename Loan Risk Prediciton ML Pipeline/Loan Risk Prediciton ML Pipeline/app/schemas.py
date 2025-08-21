"""
Pydantic schemas for the Loan Risk Prediction API.

This module defines the data models for input validation and response formatting
for the loan risk prediction endpoints.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re


class BorrowerFeatures(BaseModel):
    """
    Input schema for borrower features matching the actual dataset columns.
    
    This schema matches the exact column names and structure from the dataset:
    LoanID, Age, Income, LoanAmount, CreditScore, MonthsEmployed, NumCreditLines,
    InterestRate, LoanTerm, DTIRatio, Education, EmploymentType, MaritalStatus,
    HasMortgage, HasDependents, LoanPurpose, HasCoSigner, Default
    """
    
    # Note: LoanID is auto-generated, not required as input
    Age: int = Field(..., ge=18, le=100, description="Age of the borrower")
    Income: float = Field(..., gt=0, description="Annual income")
    LoanAmount: float = Field(..., gt=0, description="Requested loan amount")
    CreditScore: int = Field(..., ge=300, le=850, description="Credit score")
    MonthsEmployed: int = Field(..., ge=0, le=600, description="Months of employment")
    NumCreditLines: int = Field(..., ge=0, le=50, description="Number of credit lines")
    InterestRate: float = Field(..., gt=0, le=30, description="Interest rate percentage")
    LoanTerm: int = Field(..., ge=6, le=84, description="Loan term in months")
    DTIRatio: float = Field(..., ge=0, le=1, description="Debt to income ratio (0-1)")
    Education: str = Field(..., description="Education level")
    EmploymentType: str = Field(..., description="Employment type")
    MaritalStatus: str = Field(..., description="Marital status")
    HasMortgage: str = Field(..., description="Has mortgage (Yes/No)")
    HasDependents: str = Field(..., description="Has dependents (Yes/No)")
    LoanPurpose: str = Field(..., description="Purpose of the loan")
    HasCoSigner: str = Field(..., description="Has co-signer (Yes/No)")
    
    @validator('Education')
    def validate_education(cls, v):
        """Validate education values based on dataset."""
        valid_values = {"High School", "Bachelor's", "Master's", "PhD"}
        if v not in valid_values:
            raise ValueError(f'Invalid education. Must be one of: {valid_values}')
        return v
    
    @validator('EmploymentType')
    def validate_employment_type(cls, v):
        """Validate employment type values based on dataset."""
        valid_values = {"Full-time", "Part-time", "Self-employed", "Unemployed"}
        if v not in valid_values:
            raise ValueError(f'Invalid employment type. Must be one of: {valid_values}')
        return v
    
    @validator('MaritalStatus')
    def validate_marital_status(cls, v):
        """Validate marital status values based on dataset."""
        valid_values = {"Single", "Married", "Divorced"}
        if v not in valid_values:
            raise ValueError(f'Invalid marital status. Must be one of: {valid_values}')
        return v
    
    @validator('HasMortgage', 'HasDependents', 'HasCoSigner')
    def validate_yes_no_fields(cls, v):
        """Validate Yes/No fields."""
        valid_values = {"Yes", "No"}
        if v not in valid_values:
            raise ValueError(f'Must be "Yes" or "No"')
        return v
    
    @validator('LoanPurpose')
    def validate_loan_purpose(cls, v):
        """Validate loan purpose values based on dataset."""
        valid_values = {"Home", "Auto", "Personal", "Education", "Other"}
        if v not in valid_values:
            raise ValueError(f'Invalid loan purpose. Must be one of: {valid_values}')
        return v

    class Config:
        """Pydantic configuration."""
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "Age": 35,
                "Income": 75000,
                "LoanAmount": 25000,
                "CreditScore": 720,
                "MonthsEmployed": 96,
                "NumCreditLines": 5,
                "InterestRate": 12.5,
                "LoanTerm": 60,
                "DTIRatio": 0.25,
                "Education": "Bachelor's",
                "EmploymentType": "Full-time",
                "MaritalStatus": "Single",
                "HasMortgage": "No",
                "HasDependents": "No",
                "LoanPurpose": "Other",
                "HasCoSigner": "No"
            }
        }


class RiskPredictionResponse(BaseModel):
    """
    Response schema for risk prediction endpoint.
    
    Contains the predicted risk score, risk category, and additional metadata.
    """
    
    risk_score: float = Field(..., ge=0, le=1, description="Probability of default (0-1)")
    risk_category: str = Field(..., description="Risk category based on score")
    confidence_interval: Optional[Dict[str, float]] = Field(None, description="95% confidence interval")
    recommendation: str = Field(..., description="Lending recommendation")
    factors: Dict[str, Any] = Field(..., description="Key factors influencing the prediction")
    timestamp: datetime = Field(default_factory=datetime.now, description="Prediction timestamp")
    model_version: str = Field(..., description="Version of the model used")
    
    @validator('risk_category', pre=True, always=True)
    def determine_risk_category(cls, v, values):
        """Determine risk category based on risk score."""
        if 'risk_score' in values:
            score = values['risk_score']
            if score < 0.2:
                return "LOW"
            elif score < 0.5:
                return "MEDIUM"
            elif score < 0.7:
                return "HIGH"
            else:
                return "VERY_HIGH"
        return v
    
    @validator('recommendation', pre=True, always=True)
    def determine_recommendation(cls, v, values):
        """Determine lending recommendation based on risk score."""
        if 'risk_score' in values:
            score = values['risk_score']
            if score < 0.3:
                return "APPROVE"
            elif score < 0.6:
                return "REVIEW"
            else:
                return "DECLINE"
        return v

    class Config:
        """Pydantic configuration."""
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "risk_score": 0.15,
                "risk_category": "LOW",
                "confidence_interval": {"lower": 0.12, "upper": 0.18},
                "recommendation": "APPROVE",
                "factors": {
                    "top_positive_factors": ["High credit score", "Low debt-to-income ratio"],
                    "top_negative_factors": ["Short employment length"],
                    "feature_contributions": {"credit_score": -0.05, "debt_to_income_ratio": -0.03}
                },
                "timestamp": "2024-01-15T10:30:00",
                "model_version": "stacking_v1.0"
            }
        }


class ModelPerformanceResponse(BaseModel):
    """
    Response schema for model performance endpoint.
    
    Contains model performance metrics and feature importance information.
    """
    
    model_info: Dict[str, Any] = Field(..., description="General model information")
    performance_metrics: Dict[str, float] = Field(..., description="Model performance metrics")
    feature_importance: List[Dict[str, Union[str, float]]] = Field(..., description="Top important features")
    data_info: Dict[str, Any] = Field(..., description="Training data information")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last model update")
    
    class Config:
        """Pydantic configuration."""
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "model_info": {
                    "model_type": "Stacking Classifier",
                    "base_models": ["LightGBM", "XGBoost", "Logistic Regression"],
                    "meta_learner": "Logistic Regression",
                    "version": "1.0.0"
                },
                "performance_metrics": {
                    "auc_roc": 0.8745,
                    "f1_score": 0.7234,
                    "precision": 0.7891,
                    "recall": 0.6678,
                    "accuracy": 0.8234
                },
                "feature_importance": [
                    {"feature": "credit_score", "importance": 0.1245},
                    {"feature": "debt_to_income_ratio", "importance": 0.0987},
                    {"feature": "annual_income", "importance": 0.0876}
                ],
                "data_info": {
                    "training_samples": 50000,
                    "features_count": 25,
                    "class_imbalance_ratio": 7.1
                },
                "last_updated": "2024-01-15T08:00:00"
            }
        }


class BatchPredictionRequest(BaseModel):
    """
    Schema for batch prediction requests.
    
    Allows multiple borrower records to be processed at once.
    """
    
    borrowers: List[BorrowerFeatures] = Field(..., description="List of borrower features")
    include_details: bool = Field(default=True, description="Include detailed factor analysis")
    
    @validator('borrowers')
    def validate_batch_size(cls, v):
        """Validate batch size limits."""
        if len(v) > 100:
            raise ValueError("Batch size cannot exceed 100 records")
        if len(v) == 0:
            raise ValueError("At least one borrower record is required")
        return v

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "borrowers": [
                    {
                        "Age": 35,
                        "Income": 75000,
                        "LoanAmount": 25000,
                        "CreditScore": 720,
                        "MonthsEmployed": 96,
                        "NumCreditLines": 5,
                        "InterestRate": 12.5,
                        "LoanTerm": 60,
                        "DTIRatio": 0.25,
                        "Education": "Bachelor's",
                        "EmploymentType": "Full-time",
                        "MaritalStatus": "Single",
                        "HasMortgage": "No",
                        "HasDependents": "No",
                        "LoanPurpose": "Other",
                        "HasCoSigner": "No"
                    }
                ],
                "include_details": True
            }
        }


class BatchPredictionResponse(BaseModel):
    """
    Response schema for batch prediction requests.
    """
    
    predictions: List[RiskPredictionResponse] = Field(..., description="Predictions for each borrower")
    summary: Dict[str, Any] = Field(..., description="Batch processing summary")
    processing_time: float = Field(..., description="Total processing time in seconds")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "predictions": [
                    {
                        "risk_score": 0.15,
                        "risk_category": "LOW",
                        "recommendation": "APPROVE",
                        "factors": {"top_positive_factors": ["High credit score"]},
                        "timestamp": "2024-01-15T10:30:00",
                        "model_version": "stacking_v1.0"
                    }
                ],
                "summary": {
                    "total_processed": 1,
                    "approve_count": 1,
                    "review_count": 0,
                    "decline_count": 0,
                    "average_risk_score": 0.15
                },
                "processing_time": 0.234
            }
        }


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Detailed error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid input data provided",
                "details": {
                    "field": "credit_score",
                    "issue": "Value must be between 300 and 850"
                },
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class HealthCheckResponse(BaseModel):
    """
    Schema for health check endpoint response.
    """
    
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether the ML model is loaded")
    dependencies: Dict[str, str] = Field(..., description="Status of dependencies")
    
    class Config:
        """Pydantic configuration."""
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00",
                "version": "1.0.0",
                "model_loaded": True,
                "dependencies": {
                    "database": "connected",
                    "model_file": "loaded",
                    "feature_store": "accessible"
                }
            }
        }
