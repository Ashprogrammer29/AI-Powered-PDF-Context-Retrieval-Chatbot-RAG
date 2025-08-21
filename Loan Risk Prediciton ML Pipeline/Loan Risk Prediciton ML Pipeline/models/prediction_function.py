
def predict_loan_default(features, model_path="../models/loan_risk_model.pkl", 
                        scaler_path="../models/feature_scaler.pkl"):
    """
    Predict loan default probability

    Args:
        features: dict with feature values
        model_path: path to saved model
        scaler_path: path to saved scaler

    Returns:
        dict with prediction and probability
    """
    import joblib
    import numpy as np
    import pandas as pd

    # Load model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    # Expected feature order
    feature_names = ['Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio', 'LoanToIncome_Ratio', 'MonthlyPayment_Est', 'PaymentToIncome_Ratio', 'CreditLines_Per_Year', 'Employment_Stability', 'HighRate_LowCredit', 'YoungHighDebt', 'Age_Squared', 'Income_Log', 'CreditScore_Cubed', 'Age_Income_Interaction', 'Rate_Term_Interaction', 'Age_Group_encoded', 'Income_Quartile_encoded', 'LoanAmount_Quartile_encoded']

    # Convert features to array in correct order
    feature_array = np.array([features[name] for name in feature_names]).reshape(1, -1)

    # Scale features
    feature_array_scaled = scaler.transform(feature_array)

    # Predict
    prediction = model.predict(feature_array_scaled)[0]
    probability = model.predict_proba(feature_array_scaled)[0, 1]

    return {
        "prediction": int(prediction),
        "default_probability": float(probability),
        "risk_level": "High" if probability > 0.5 else "Medium" if probability > 0.2 else "Low"
    }
