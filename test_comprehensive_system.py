#!/usr/bin/env python3
"""
Comprehensive test script for the Breast Cancer AI Prediction System
Tests all endpoints and functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_models():
    """Test models endpoint"""
    print("🔍 Testing models endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            data = response.json()
            loaded_models = data.get('loaded_models', 0)
            total_models = data.get('total_models', 0)
            print(f"✅ Models endpoint working - {loaded_models}/{total_models} models loaded")
            return True
        else:
            print(f"❌ Models endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Models endpoint error: {e}")
        return False

def test_predict_all():
    """Test comprehensive prediction endpoint"""
    print("🔍 Testing comprehensive prediction endpoint...")
    
    # Sample data
    sample_features = {
        "feature_1": 0.5,
        "feature_2": 0.3,
        "feature_3": 0.7,
        "feature_4": 0.2,
        "feature_5": 0.8,
        "feature_6": 0.4,
        "feature_7": 0.6,
        "feature_8": 0.1,
        "feature_9": 0.9,
        "feature_10": 0.3,
        "feature_11": 0.5,
        "feature_12": 0.7,
        "feature_13": 0.2,
        "feature_14": 0.8,
        "feature_15": 0.4,
        "feature_16": 0.6,
        "feature_17": 0.1,
        "feature_18": 0.9,
        "feature_19": 0.3,
        "feature_20": 0.5
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict-all",
            json={"features": sample_features},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            successful_predictions = data.get('successful_predictions', 0)
            total_targets = data.get('total_targets', 0)
            print(f"✅ Comprehensive prediction working - {successful_predictions}/{total_targets} successful")
            return True
        else:
            print(f"❌ Comprehensive prediction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Comprehensive prediction error: {e}")
        return False

def test_batch_predict_all():
    """Test batch comprehensive prediction endpoint"""
    print("🔍 Testing batch comprehensive prediction endpoint...")
    
    # Sample batch data
    batch_data = [
        {
            "feature_1": 0.5, "feature_2": 0.3, "feature_3": 0.7,
            "feature_4": 0.2, "feature_5": 0.8, "feature_6": 0.4,
            "feature_7": 0.6, "feature_8": 0.1, "feature_9": 0.9,
            "feature_10": 0.3, "feature_11": 0.5, "feature_12": 0.7,
            "feature_13": 0.2, "feature_14": 0.8, "feature_15": 0.4,
            "feature_16": 0.6, "feature_17": 0.1, "feature_18": 0.9,
            "feature_19": 0.3, "feature_20": 0.5
        },
        {
            "feature_1": 0.2, "feature_2": 0.8, "feature_3": 0.4,
            "feature_4": 0.6, "feature_5": 0.1, "feature_6": 0.9,
            "feature_7": 0.3, "feature_8": 0.5, "feature_9": 0.7,
            "feature_10": 0.2, "feature_11": 0.8, "feature_12": 0.4,
            "feature_13": 0.6, "feature_14": 0.1, "feature_15": 0.9,
            "feature_16": 0.3, "feature_17": 0.5, "feature_18": 0.7,
            "feature_19": 0.2, "feature_20": 0.8
        }
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/batch-predict-all",
            json={"data": batch_data},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            total_cases = data.get('total_cases', 0)
            successful_predictions = data.get('successful_predictions', 0)
            print(f"✅ Batch comprehensive prediction working - {successful_predictions} predictions for {total_cases} cases")
            return True
        else:
            print(f"❌ Batch comprehensive prediction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Batch comprehensive prediction error: {e}")
        return False

def test_individual_endpoints():
    """Test individual prediction endpoints"""
    print("🔍 Testing individual prediction endpoints...")
    
    sample_features = {
        "feature_1": 0.5, "feature_2": 0.3, "feature_3": 0.7,
        "feature_4": 0.2, "feature_5": 0.8, "feature_6": 0.4,
        "feature_7": 0.6, "feature_8": 0.1, "feature_9": 0.9,
        "feature_10": 0.3, "feature_11": 0.5, "feature_12": 0.7,
        "feature_13": 0.2, "feature_14": 0.8, "feature_15": 0.4,
        "feature_16": 0.6, "feature_17": 0.1, "feature_18": 0.9,
        "feature_19": 0.3, "feature_20": 0.5
    }
    
    endpoints = [
        "/predict-vital-status",
        "/predict-cancer-type",
        "/predict-stage",
        "/predict-metastasis",
        "/predict-treatment-outcome",
        "/predict-treatment-type",
        "/predict-clinical-trial",
        "/predict-age-at-index",
        "/predict-classification-of-tumor",
        "/predict-disease-response",
        "/predict-tissue-or-organ-of-origin"
    ]
    
    successful = 0
    total = len(endpoints)
    
    for endpoint in endpoints:
        try:
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json={"features": sample_features},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"✅ {endpoint} working")
                successful += 1
            else:
                print(f"❌ {endpoint} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")
    
    print(f"Individual endpoints: {successful}/{total} successful")
    return successful == total

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive system test...")
    print("=" * 50)
    
    tests = [
        test_health,
        test_models,
        test_predict_all,
        test_batch_predict_all,
        test_individual_endpoints
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
            print()
    
    print("=" * 50)
    print("📊 Test Results Summary:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! System is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the system.")
    
    return all(results)

if __name__ == "__main__":
    main() 