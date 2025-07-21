import joblib
import csv
import os

# Map of target to feature_names file
target_files = {
    'stage': 'feature_names_stage.joblib',
    'metastasis': 'feature_names_metastasis.joblib',
    'cancer_type': 'feature_names_cancer_type.joblib',
    'age_at_index': 'feature_names_age_at_index.joblib',
    'vital_status': 'feature_names_vital_status.joblib',
    'clinical_trial': 'feature_names_clinical_trial.joblib',
    'treatment_type': 'feature_names_treatment_type.joblib',
    'disease_response': 'feature_names_disease_response.joblib',
    'treatment_outcome': 'feature_names_treatment_outcome.joblib',
    'classification_of_tumor': 'feature_names_classification_of_tumor.joblib',
    'tissue_or_organ_of_origin': 'feature_names_tissue_or_organ_of_origin.joblib',
}

# Output directory for sample CSVs
output_dir = 'frontend/public/'
os.makedirs(output_dir, exist_ok=True)

for target, fname in target_files.items():
    features = joblib.load(fname)
    # Create a row of placeholder/example data (0 for numeric, empty for string)
    row = []
    for f in features:
        # Simple heuristic: if 'age', 'days', 'size', 'count', 'number', 'score', 'percent', 'year', 'duration', 'weight', 'dimension', 'dose', 'height', 'width', 'length', 'thickness', 'distance' in name, use 0, else empty string
        if any(x in f for x in ['age', 'days', 'size', 'count', 'number', 'score', 'percent', 'year', 'duration', 'weight', 'dimension', 'dose', 'height', 'width', 'length', 'thickness', 'distance']):
            row.append(0)
        else:
            row.append("")
    out_path = os.path.join(output_dir, f'sample_{target}.csv')
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(features)
        writer.writerow(row)
    print(f"Wrote {out_path} with {len(features)} columns.") 