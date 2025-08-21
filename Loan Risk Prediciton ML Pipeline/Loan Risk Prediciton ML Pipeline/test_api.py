"""
Test script for the Loan Risk Prediction API.

This script tests the main endpoints of the API to ensure they work correctly.
"""

import requests
import json
import time
from typing import Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check() -> bool:
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print("✅ Health Check:")
        print(f"   Status: {data['status']}")
        print(f"   Model Loaded: {data['model_loaded']}")
        print(f"   Version: {data['version']}")
        
        return data['status'] == 'healthy' and data['model_loaded']
        
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_single_prediction() -> bool:
    """Test single prediction endpoint."""
    try:
        # Sample borrower data using actual dataset column names
        borrower_data = {
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
        
        response = requests.post(
            f"{BASE_URL}/predict",
            json=borrower_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        print("✅ Single Prediction:")
        print(f"   Risk Score: {data['risk_score']:.3f}")
        print(f"   Risk Category: {data['risk_category']}")
        print(f"   Recommendation: {data['recommendation']}")
        print(f"   Top Positive Factors: {data['factors'].get('top_positive_factors', [])}")
        
        return 0 <= data['risk_score'] <= 1
        
    except Exception as e:
        print(f"❌ Single Prediction Failed: {e}")
        return False

def test_batch_prediction() -> bool:
    """Test batch prediction endpoint."""
    try:
        # Sample batch data using actual dataset column names
        batch_data = {
            "borrowers": [
                {
                    "Age": 25,
                    "Income": 45000,
                    "LoanAmount": 20000,
                    "CreditScore": 620,
                    "MonthsEmployed": 24,
                    "NumCreditLines": 3,
                    "InterestRate": 15.0,
                    "LoanTerm": 48,
                    "DTIRatio": 0.35,
                    "Education": "High School",
                    "EmploymentType": "Full-time",
                    "MaritalStatus": "Single",
                    "HasMortgage": "No",
                    "HasDependents": "No",
                    "LoanPurpose": "Auto",
                    "HasCoSigner": "No"
                },
                {
                    "Age": 45,
                    "Income": 90000,
                    "LoanAmount": 30000,
                    "CreditScore": 780,
                    "MonthsEmployed": 180,
                    "NumCreditLines": 7,
                    "InterestRate": 8.5,
                    "LoanTerm": 60,
                    "DTIRatio": 0.15,
                    "Education": "Master's",
                    "EmploymentType": "Full-time",
                    "MaritalStatus": "Married",
                    "HasMortgage": "Yes",
                    "HasDependents": "Yes",
                    "LoanPurpose": "Home",
                    "HasCoSigner": "No"
                }
            ],
            "include_details": True
        }
        
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json=batch_data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        data = response.json()
        print("✅ Batch Prediction:")
        print(f"   Total Processed: {data['summary']['total_processed']}")
        print(f"   Approve Count: {data['summary']['approve_count']}")
        print(f"   Review Count: {data['summary']['review_count']}")
        print(f"   Decline Count: {data['summary']['decline_count']}")
        print(f"   Average Risk Score: {data['summary']['average_risk_score']}")
        print(f"   Processing Time: {data['processing_time']}s")
        
        return len(data['predictions']) == 2
        
    except Exception as e:
        print(f"❌ Batch Prediction Failed: {e}")
        return False

def test_model_performance() -> bool:
    """Test model performance endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/model/performance")
        response.raise_for_status()
        
        data = response.json()
        print("✅ Model Performance:")
        print(f"   Model Type: {data['model_info']['model_type']}")
        print(f"   AUC-PR: {data['performance_metrics']['auc_pr']:.4f}")
        print(f"   AUC-ROC: {data['performance_metrics']['auc_roc']:.4f}")
        print(f"   Training Samples: {data['data_info']['training_samples']:,}")
        print(f"   Features Count: {data['data_info']['features_count']}")
        
        return data['performance_metrics']['auc_pr'] > 0
        
    except Exception as e:
        print(f"❌ Model Performance Failed: {e}")
        return False

def test_error_handling() -> bool:
    """Test error handling with invalid data."""
    try:
        # Invalid data (negative age and invalid categorical values)
        invalid_data = {
            "Age": -5,
            "Income": 75000,
            "LoanAmount": 25000,
            "CreditScore": 720,
            "MonthsEmployed": 96,
            "NumCreditLines": 5,
            "InterestRate": 12.5,
            "LoanTerm": 60,
            "DTIRatio": 0.25,
            "Education": "INVALID",
            "EmploymentType": "INVALID",
            "MaritalStatus": "Single",
            "HasMortgage": "No",
            "HasDependents": "No",
            "LoanPurpose": "Other",
            "HasCoSigner": "No"
        }
        
        response = requests.post(
            f"{BASE_URL}/predict",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Should return 422 for validation error
        if response.status_code == 422:
            print("✅ Error Handling: Correctly rejected invalid data")
            return True
        else:
            print(f"❌ Error Handling: Expected 422, got {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error Handling Test Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing AI-Powered Loan Risk Scoring API")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health_check),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
        ("Model Performance", test_model_performance),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the API server and logs.")
        return 1

if __name__ == "__main__":
    exit(main())
