import requests
import json
import joblib

def test_backend():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health error: {e}")
    
    # Test models endpoint
    print("\nTesting models endpoint...")
    try:
        response = requests.get(f"{base_url}/models")
        print(f"Models: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Loaded models: {data.get('loaded_models', 0)}/{data.get('total_models', 0)}")
    except Exception as e:
        print(f"Models error: {e}")
    
    # Test individual endpoints first
    print("\nTesting individual endpoints...")
    targets = ['vital_status', 'cancer_type', 'stage']
    
    for target in targets:
        try:
            # Load actual feature names for this target
            features = joblib.load(f'feature_names_{target}.joblib')
            print(f"\n{target}: Using {len(features)} features")
            
            # Create sample data with actual feature names
            sample_data = {}
            for feature in features:
                sample_data[feature] = 0.5  # Use 0.5 as default value
            
            response = requests.post(
                f"{base_url}/predict-{target.replace('_', '-')}",
                json={"features": sample_data},
                headers={"Content-Type": "application/json"}
            )
            print(f"  {target}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Prediction: {data.get('prediction')}")
            else:
                print(f"  Error: {response.text[:200]}")
        except Exception as e:
            print(f"  {target} error: {e}")
    
    # Test predict-all endpoint with comprehensive feature set
    print("\nTesting predict-all endpoint...")
    try:
        # Get all unique features from all models
        all_features = set()
        for target in ['vital_status', 'cancer_type', 'stage', 'metastasis', 'treatment_outcome']:
            try:
                features = joblib.load(f'feature_names_{target}.joblib')
                all_features.update(features)
            except:
                pass
        
        print(f"Using {len(all_features)} unique features")
        
        # Create sample data with all features
        sample_data = {}
        for feature in all_features:
            sample_data[feature] = 0.5  # Use 0.5 as default value
        
        response = requests.post(
            f"{base_url}/predict-all",
            json={"features": sample_data},
            headers={"Content-Type": "application/json"}
        )
        print(f"Predict-all: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Successful predictions: {data.get('successful_predictions', 0)}/{data.get('total_targets', 0)}")
            
            # Show some prediction results
            predictions = data.get('predictions', {})
            for target, result in list(predictions.items())[:3]:  # Show first 3
                if result.get('error'):
                    print(f"  {target}: {result['error']}")
                else:
                    print(f"  {target}: {result.get('prediction')} (confidence: {result.get('confidence', 0):.3f})")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Predict-all error: {e}")

if __name__ == "__main__":
    test_backend() 