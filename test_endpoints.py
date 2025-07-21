import requests
import json
import pandas as pd
import numpy as np

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model_info():
    """Test the model info endpoint"""
    print("\n📊 Testing model info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Available endpoints: {data.get('available_endpoints', [])}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def create_sample_features():
    """Create sample feature data for testing"""
    # Create a sample feature vector with 370 features (matching our dataset)
    features = {}
    for i in range(370):
        features[f"feature_{i}"] = np.random.random()
    return features

def test_vital_status_endpoints():
    """Test vital status prediction endpoints"""
    print("\n💓 Testing vital status endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-vital-status", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-vital-status", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_cancer_type_endpoints():
    """Test cancer type prediction endpoints"""
    print("\n🔬 Testing cancer type endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-cancer-type", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-cancer-type", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_stage_endpoints():
    """Test stage prediction endpoints"""
    print("\n📈 Testing stage endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-stage", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-stage", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_metastasis_endpoints():
    """Test metastasis prediction endpoints"""
    print("\n🔄 Testing metastasis endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-metastasis", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-metastasis", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_treatment_outcome_endpoints():
    """Test treatment outcome prediction endpoints"""
    print("\n💊 Testing treatment outcome endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-treatment-outcome", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-treatment-outcome", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_treatment_type_endpoints():
    """Test treatment type prediction endpoints"""
    print("\n🏥 Testing treatment type endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-treatment-type", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-treatment-type", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_clinical_trial_endpoints():
    """Test clinical trial prediction endpoints"""
    print("\n🧪 Testing clinical trial endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-clinical-trial", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-clinical-trial", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_age_at_index_endpoints():
    """Test age at index prediction endpoints"""
    print("\n👴 Testing age at index endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-age-at-index", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-age-at-index", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_classification_of_tumor_endpoints():
    """Test classification of tumor prediction endpoints"""
    print("\n🔬 Testing classification of tumor endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-classification-of-tumor", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-classification-of-tumor", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_disease_response_endpoints():
    """Test disease response prediction endpoints"""
    print("\n📊 Testing disease response endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-disease-response", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-disease-response", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_tissue_or_organ_of_origin_endpoints():
    """Test tissue or organ of origin prediction endpoints"""
    print("\n🏥 Testing tissue or organ of origin endpoints...")
    
    # Test single prediction
    print("   Testing single prediction...")
    sample_features = create_sample_features()
    payload = {"features": sample_features}
    
    try:
        response = requests.post(f"{BASE_URL}/predict-tissue-or-organ-of-origin", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Prediction: {data.get('prediction')}")
            print(f"   Probabilities: {data.get('probabilities')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test batch prediction
    print("   Testing batch prediction...")
    batch_payload = {
        "data": [
            sample_features,  # Direct feature dict, not wrapped in 'features'
            sample_features
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/batch-predict-tissue-or-organ-of-origin", json=batch_payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Predictions: {data.get('predictions')}")
            print(f"   Number of cases: {data.get('n_cases')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Breast Cancer AI API Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    health_ok = test_health()
    info_ok = test_model_info()
    
    if not health_ok:
        print("❌ Health check failed. Make sure the API server is running on http://localhost:8000")
        return
    
    # Test prediction endpoints
    test_vital_status_endpoints()
    test_cancer_type_endpoints()
    test_stage_endpoints()
    test_metastasis_endpoints()
    test_treatment_outcome_endpoints()
    test_treatment_type_endpoints()
    test_clinical_trial_endpoints()
    test_age_at_index_endpoints()
    test_classification_of_tumor_endpoints()
    test_disease_response_endpoints()
    test_tissue_or_organ_of_origin_endpoints()
    
    print("\n✅ Endpoint testing completed!")

if __name__ == "__main__":
    main() 