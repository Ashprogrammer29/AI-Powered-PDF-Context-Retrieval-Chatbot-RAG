"""
Configuration settings for the Loan Risk Prediction API.

This module handles environment variables and application configuration.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "AI-Powered Loan Risk Scoring API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Model Configuration
    models_dir: str = "models"
    model_file: str = "loan_risk_model.pkl"
    scaler_file: str = "feature_scaler.pkl"
    metadata_file: str = "model_metadata.json"
    
    # Prediction Configuration
    max_batch_size: int = 100
    prediction_timeout: int = 30  # seconds
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security Configuration
    api_key: Optional[str] = None
    rate_limit: str = "100/minute"
    
    # Monitoring Configuration
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Database Configuration (for future use)
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    
    # Model Retraining Configuration
    retrain_threshold_accuracy: float = 0.85
    retrain_check_interval: int = 24  # hours
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in Pydantic v2
        protected_namespaces = ('settings_',)


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_models_dir() -> Path:
    """Get the models directory path."""
    settings = get_settings()
    return get_project_root() / settings.models_dir


# Global settings instance
settings = get_settings()
