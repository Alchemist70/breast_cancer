import requests
import joblib

def debug_predict_all():
    base_url = "http://localhost:8000"
    
    # Test with just vital_status features first
    try:
        vital_features = joblib.load('feature_names_vital_status.joblib')
        print(f"Testing with {len(vital_features)} vital_status features")
        
        sample_data = {}
        for feature in vital_features:
            sample_data[feature] = 0.5
        
        response = requests.post(
            f"{base_url}/predict-all",
            json={"features": sample_data},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            data = response.json()
            print(f"Success: {data.get('successful_predictions', 0)}/{data.get('total_targets', 0)}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_predict_all() 