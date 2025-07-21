import os
import json
import joblib
import pandas as pd

# This script standardizes all sample CSV files based on the authoritative feature lists
# from the model's .joblib or .json files. It also generates a new, unified
# sample_data.csv for the "All Predictions" tab.

# --- Configuration ---
MODELS_CONFIG = {
    "wdbc_malignancy": {
        "features_path": "wdbc_malignancy_features.joblib",
        "sample_file": "sample_wdbc_malignancy.csv",
    },
    "vital_status": {
        "features_path": "feature_names_vital_status.joblib",
        "sample_file": "sample_vital_status.csv",
    },
    "cancer_type": {
        "features_path": "feature_names_cancer_type.joblib",
        "sample_file": "sample_cancer_type.csv",
    },
    "stage": {
        "features_path": "feature_names_stage.joblib",
        "sample_file": "sample_stage.csv",
    },
    "metastasis": {
        "features_path": "feature_names_metastasis.joblib",
        "sample_file": "sample_metastasis.csv",
    },
    "treatment_outcome": {
        "features_path": "feature_names_treatment_outcome.joblib",
        "sample_file": "sample_treatment_outcome.csv",
    },
    "treatment_type": {
        "features_path": "feature_names_treatment_type.joblib",
        "sample_file": "sample_treatment_type.csv",
    },
    "clinical_trial": {
        "features_path": "feature_names_clinical_trial.joblib",
        "sample_file": "sample_clinical_trial.csv",
    },
    "age_at_index": {
        "features_path": "feature_names_age_at_index.joblib",
        "sample_file": "sample_age_at_index.csv",
    },
    "classification_of_tumor": {
        "features_path": "feature_names_classification_of_tumor.joblib",
        "sample_file": "sample_classification_of_tumor.csv",
    },
    "disease_response": {
        "features_path": "feature_names_disease_response.joblib",
        "sample_file": "sample_disease_response.csv",
    },
    "tissue_or_organ_of_origin": {
        "features_path": "feature_names_tissue_or_organ_of_origin.joblib",
        "sample_file": "sample_tissue_or_organ_of_origin.csv",
    },
}

OUTPUT_DIR = "frontend/public"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Main Logic ---

all_features = set()
feature_lists = {}

# 1. Load all feature lists from their source files
for target, config in MODELS_CONFIG.items():
    try:
        if config["features_path"].endswith(".json"):
            with open(config["features_path"], "r") as f:
                features = json.load(f)
        else:
            features = joblib.load(config["features_path"])
        
        if isinstance(features, list):
            feature_lists[target] = features
            all_features.update(features)
        else:
            print(f"⚠️  Warning: Features for '{target}' is not a list. Skipping.")

    except FileNotFoundError:
        print(f"❌ Error: Feature file not found for '{target}': {config['features_path']}")
    except Exception as e:
        print(f"❌ Error loading features for '{target}': {e}")

# 2. Generate a realistic sample row for all unique features
all_features_list = sorted(list(all_features))
unified_sample_row = {}
for feature in all_features_list:
    # Use more realistic, varied, and non-zero values
    if "year" in feature or "age" in feature:
        unified_sample_row[feature] = 55
    elif "day" in feature:
        unified_sample_row[feature] = 100
    elif "size" in feature or "radius" in feature or "perimeter" in feature:
        unified_sample_row[feature] = 15.0 + (hash(feature) % 100) / 10.0
    elif "area" in feature:
        unified_sample_row[feature] = 400.0 + (hash(feature) % 1000)
    elif "concave" in feature or "concavity" in feature:
         unified_sample_row[feature] = 0.05 + (hash(feature) % 100) / 1000.0
    else:
        unified_sample_row[feature] = 0.5 + (hash(feature) % 100) / 100.0

# 3. Create individual sample CSVs for each model
for target, features in feature_lists.items():
    config = MODELS_CONFIG[target]
    df_data = {}
    for feature in features:
        # Ensure every feature has a value
        df_data[feature] = [unified_sample_row.get(feature, 1.0)]

    df = pd.DataFrame(df_data)
    output_path = os.path.join(OUTPUT_DIR, config["sample_file"])
    df.to_csv(output_path, index=False, lineterminator='\n')
    print(f"✅ Generated sample file: {output_path}")

# 4. Create a unified sample_data.csv for the "All Predictions" tab
unified_df = pd.DataFrame([unified_sample_row], columns=all_features_list)
unified_output_path = os.path.join(OUTPUT_DIR, "sample_data.csv")
unified_df.to_csv(unified_output_path, index=False, lineterminator='\n')
print(f"✅ Generated unified sample file: {unified_output_path}")

print("\n🎉 All sample files have been regenerated successfully.") 