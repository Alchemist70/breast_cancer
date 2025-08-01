from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import joblib
import json
import io
from typing import List, Dict, Optional, Any
import uvicorn
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
import asyncio
import threading

# Initialize FastAPI app
app = FastAPI(
    title="Breast Cancer AI Prediction API",
    description="AI-powered breast cancer prediction and analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Unified Model Management (This must come before endpoints) ---
MODELS_CONFIG = {
    'wdbc_malignancy': {
        'model_path': 'wdbc_malignancy_model.joblib',
        'scaler_path': 'wdbc_malignancy_scaler.joblib',
        'features_path': 'wdbc_malignancy_features.joblib',
        'summary_path': 'model_summary_wdbc_malignancy.json',
    },
    'vital_status': {'model_path': 'vital_status_enhanced_model.joblib', 'scaler_path': 'scaler_vital_status.joblib', 'features_path': 'feature_names_vital_status.joblib', 'summary_path': 'model_summary_vital_status.json'},
    'cancer_type': {'model_path': 'cancer_type_enhanced_model.joblib', 'scaler_path': 'scaler_cancer_type.joblib', 'features_path': 'feature_names_cancer_type.joblib', 'summary_path': 'model_summary_cancer_type.json'},
    'stage': {'model_path': 'stage_enhanced_model.joblib', 'scaler_path': 'scaler_stage.joblib', 'features_path': 'feature_names_stage.joblib', 'summary_path': 'model_summary_stage.json'},
    'metastasis': {'model_path': 'metastasis_enhanced_model.joblib', 'scaler_path': 'scaler_metastasis.joblib', 'features_path': 'feature_names_metastasis.joblib', 'summary_path': 'model_summary_metastasis.json'},
    'treatment_outcome': {'model_path': 'treatment_outcome_enhanced_model.joblib', 'scaler_path': 'scaler_treatment_outcome.joblib', 'features_path': 'feature_names_treatment_outcome.joblib', 'summary_path': 'model_summary_treatment_outcome.json'},
    'treatment_type': {'model_path': 'treatment_type_enhanced_model.joblib', 'scaler_path': 'scaler_treatment_type.joblib', 'features_path': 'feature_names_treatment_type.joblib', 'summary_path': 'model_summary_treatment_type.json'},
    'clinical_trial': {'model_path': 'clinical_trial_enhanced_model.joblib', 'scaler_path': 'scaler_clinical_trial.joblib', 'features_path': 'feature_names_clinical_trial.joblib', 'summary_path': 'model_summary_clinical_trial.json'},
    'age_at_index': {'model_path': 'age_at_index_enhanced_model.joblib', 'scaler_path': 'scaler_age_at_index.joblib', 'features_path': 'feature_names_age_at_index.joblib', 'summary_path': 'model_summary_age_at_index.json'},
    'classification_of_tumor': {'model_path': 'classification_of_tumor_enhanced_model.joblib', 'scaler_path': 'scaler_classification_of_tumor.joblib', 'features_path': 'feature_names_classification_of_tumor.joblib', 'summary_path': 'model_summary_classification_of_tumor.json'},
    'disease_response': {'model_path': 'disease_response_enhanced_model.joblib', 'scaler_path': 'scaler_disease_response.joblib', 'features_path': 'feature_names_disease_response.joblib', 'summary_path': 'model_summary_disease_response.json'},
    'tissue_or_organ_of_origin': {'model_path': 'tissue_or_organ_of_origin_enhanced_model.joblib', 'scaler_path': 'scaler_tissue_or_organ_of_origin.joblib', 'features_path': 'feature_names_tissue_or_organ_of_origin.joblib', 'summary_path': 'model_summary_tissue_or_organ_of_origin.json'},
}

APP_STATE = {'models_loading': True, 'models_loaded': 0, 'total_models': len(MODELS_CONFIG)}

def load_models_background():
    """Load models in background thread"""
    global APP_STATE
    
    for key, config in MODELS_CONFIG.items():
        try:
            model = joblib.load(config['model_path'])
            scaler = joblib.load(config['scaler_path'])
            
            features = []
            if 'features_path' in config:
                if config['features_path'].endswith('.json'):
                    with open(config['features_path'], 'r') as f:
                        summary = json.load(f)
                        features = summary.get('feature_names', [])
                else:
                    features = joblib.load(config['features_path'])

            summary = {}
            if 'summary_path' in config:
                with open(config['summary_path'], 'r') as f:
                    summary = json.load(f)

            APP_STATE[key] = {
                'model': model,
                'scaler': scaler,
                'features': features,
                'summary': summary,
                'loaded': True
            }
            APP_STATE['models_loaded'] += 1
            print(f"✅ {key} model loaded successfully")
        except Exception as e:
            APP_STATE[key] = {'loaded': False, 'error': str(e)}
            print(f"❌ Error loading {key} model: {e}")
    
    APP_STATE['models_loading'] = False
    print(f"🎉 All models loaded! ({APP_STATE['models_loaded']}/{APP_STATE['total_models']})")

@app.on_event("startup")
async def startup_event():
    """Start model loading in background"""
    thread = threading.Thread(target=load_models_background)
    thread.daemon = True
    thread.start()

# Pydantic Models and Helper functions
class PredictionRequest(BaseModel):
    features: Dict[str, float]

class BatchPredictionRequest(BaseModel):
    data: List[Dict[str, Any]]

def get_model_accuracy(summary):
    if not summary: return 'N/A'
    acc = summary.get('test_accuracy')
    if acc is not None: return acc
    cr = summary.get('classification_report', {})
    return cr.get('accuracy', 'N/A')

def single_prediction_logic(key: str, request: PredictionRequest):
    if not APP_STATE.get(key) or not APP_STATE[key]['loaded']:
        raise HTTPException(status_code=500, detail=f"Model '{key}' not loaded")
    
    config = APP_STATE[key]
    model = config['model']
    scaler = config['scaler']
    features = config['features']
    
    if not features:
        try:
            features = scaler.get_feature_names_out()
        except AttributeError:
            raise HTTPException(status_code=500, detail=f"Could not determine features for model '{key}'")

    features_data = {feat: [request.features.get(feat, 0)] for feat in features}
    features_df = pd.DataFrame(features_data)

    features_scaled = scaler.transform(features_df)
    prediction_index = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    confidence = max(probabilities)

    class_labels = config.get('summary', {}).get('class_names')
    prediction_label = str(prediction_index)
    if class_labels and isinstance(prediction_index, (int, np.integer)) and prediction_index < len(class_labels):
        prediction_label = class_labels[prediction_index]
        
        return {
        "prediction": prediction_label,
        "prediction_index": int(prediction_index),
        "probabilities": probabilities.tolist(),
        "confidence": float(confidence),
        "model_accuracy": get_model_accuracy(config['summary'])
    }


# --- API Endpoints ---
api_router = APIRouter(prefix="/api")

@api_router.get("/models")
def get_available_models():
    available_models = {}
    for key, state in APP_STATE.items():
        if state['loaded']:
            available_models[key] = {
                "loaded": True,
                "accuracy": get_model_accuracy(state['summary']),
                "features_count": len(state['features']),
                "model_type": str(type(state['model'])).split('.')[-1][:-2],
                "summary": state['summary']
            }
        else:
            available_models[key] = {"loaded": False, "error": state['error']}
        return {
        "available_models": available_models,
        "total_models": len(MODELS_CONFIG),
        "loaded_models": sum(1 for state in APP_STATE.values() if state['loaded'])
    }

@api_router.post("/predict-all")
async def predict_all_targets(request: PredictionRequest):
    results = {}
    CONFIDENCE_THRESHOLD = 0.3
    is_benign = False

    try:
        malignancy_result = single_prediction_logic('wdbc_malignancy', request)
        results['wdbc_malignancy'] = malignancy_result
        if malignancy_result.get('prediction') == 'Benign':
            is_benign = True
    except Exception as e:
        results['wdbc_malignancy'] = {"error": f"Prediction failed: {str(e)}"}

    dependent_targets = ['stage', 'cancer_type', 'classification_of_tumor']

    for key in MODELS_CONFIG.keys():
        if key == 'wdbc_malignancy':
            continue

        if is_benign and key in dependent_targets:
            results[key] = {
                "prediction": "N/A", "confidence": 1.0,
                "model_accuracy": get_model_accuracy(APP_STATE.get(key, {}).get('summary', {})),
                "probabilities": []
            }
            continue

        try:
            if APP_STATE.get(key) and APP_STATE[key]['loaded']:
                result = single_prediction_logic(key, request)
                if "confidence" in result and result["confidence"] < CONFIDENCE_THRESHOLD and result["prediction"] != "N/A":
                    result["prediction"] = "Inconclusive"
                results[key] = result
            else:
                results[key] = {"error": APP_STATE.get(key, {}).get('error', 'Model not configured')}
        except Exception as e:
            results[key] = {"error": f"Prediction failed: {str(e)}"}

        return {
        "predictions": results,
        "total_targets": len(MODELS_CONFIG),
        "successful_predictions": sum(1 for r in results.values() if "error" not in r)
    }

@api_router.post("/batch-predict-all")
async def batch_predict_all(request: BatchPredictionRequest):
    batch_results = []
    for i, features in enumerate(request.data):
        try:
            single_request = PredictionRequest(features=features)
            result = await predict_all_targets(single_request)
            batch_results.append({"case_id": i, "predictions": result["predictions"]})
        except Exception as e:
            batch_results.append({"case_id": i, "error": str(e)})
        return {
        "batch_predictions": batch_results,
        "total_cases": len(batch_results),
        "successful_predictions": sum(1 for r in batch_results if "error" not in r)
    }

# Dynamically create single prediction endpoints for each target
for key in MODELS_CONFIG.keys():
    endpoint = f'/predict-{key.replace("_", "-")}'
    
    # This creates a closure to capture the correct 'key' for each iteration
    def create_endpoint_function(target_key):
        async def predict_target(request: PredictionRequest):
            try:
                result = single_prediction_logic(target_key, request)
                dependent_targets = ["stage", "cancer_type", "classification_of_tumor"]
                if target_key in dependent_targets:
                    malignancy_prediction = "malignant"
                    try:
                        malignancy_result = single_prediction_logic("wdbc_malignancy", request)
                        if "prediction" in malignancy_result:
                            malignancy_prediction = str(malignancy_result["prediction"]).lower()
                    except Exception:
                        pass
                    if malignancy_prediction == "benign":
                        result["prediction"] = "N/A"
                        result["confidence"] = 1.0

                if "confidence" in result and result["confidence"] < 0.3 and result["prediction"] != "N/A":
                    result["prediction"] = "Inconclusive"
                return result
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        return predict_target

    api_router.post(endpoint, name=f"predict_{key}")(create_endpoint_function(key))

app.include_router(api_router)

# --- Health Check Endpoint for Render ---
@app.get("/healthz")
def health_check():
    if APP_STATE['models_loading']:
        return {"status": "loading models", "models_loaded": APP_STATE['models_loaded'], "total_models": APP_STATE['total_models']}
    return {"status": "ok", "models_loaded": APP_STATE['models_loaded'], "total_models": APP_STATE['total_models']}

@app.get("/")
def root():
    return {"message": "Breast Cancer AI API", "status": "running"}

# --- Static Files ---
# This must be mounted AFTER the API router to avoid conflicts
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port) 