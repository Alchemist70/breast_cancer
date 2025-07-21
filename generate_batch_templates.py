import joblib
import csv
import os

def get_realistic_value(feature):
    f = feature.lower()
    if 'age' in f:
        return 55
    if 'sex' in f or 'gender' in f:
        return 0  # 0=female, 1=male
    if 'stage' in f:
        return 2
    if 'size' in f or 'diameter' in f or 'width' in f or 'length' in f or 'thickness' in f or 'dimension' in f:
        return 25
    if 'count' in f or 'number' in f or 'nodes' in f:
        return 1
    if 'grade' in f:
        return 2
    if 'status' in f:
        return 1  # 1=alive, 0=dead
    if 'outcome' in f:
        return 1  # 1=complete response
    if 'type' in f:
        return 1
    if 'trial' in f:
        return 0
    if 'response' in f:
        return 1
    if 'metastasis' in f:
        return 0
    if 'treatment' in f:
        return 1
    if 'site' in f or 'origin' in f:
        return 1
    if 'diagnosis' in f:
        return 1
    if 'smok' in f:
        return 0
    if 'exposure' in f:
        return 0
    if 'days' in f or 'year' in f:
        return 365
    if 'weight' in f:
        return 70
    if 'marital' in f:
        return 1
    if 'ethnicity' in f or 'race' in f:
        return 1
    if 'tumor' in f:
        return 1
    if 'pathologic' in f:
        return 1
    if 'score' in f:
        return 1
    if 'percent' in f:
        return 50
    if 'dose' in f:
        return 1
    if 'group' in f:
        return 1
    if 'obfuscated' in f:
        return 0
    if 'submitter' in f:
        return 1
    if 'uuid' in f:
        return 1
    if 'zone' in f:
        return 1
    if 'method' in f:
        return 1
    if 'intent' in f:
        return 1
    if 'pregnan' in f:
        return 0
    if 'pregnancy' in f:
        return 0
    if 'laterality' in f:
        return 1
    if 'shape' in f:
        return 1
    if 'level' in f:
        return 1
    if 'category' in f:
        return 1
    if 'time' in f:
        return 0
    if 'label' in f:
        return 1
    if 'pathology' in f:
        return 1
    if 'composition' in f:
        return 1
    if 'preservation' in f:
        return 1
    if 'marrow' in f:
        return 0
    if 'tobacco' in f:
        return 0
    if 'alcohol' in f:
        return 0
    if 'coal' in f:
        return 0
    if 'occupation' in f:
        return 1
    if 'biospecimen' in f:
        return 1
    if 'anatomic' in f:
        return 1
    if 'imaging' in f:
        return 0
    if 'risk' in f:
        return 1
    if 'test' in f:
        return 1
    if 'specialized' in f:
        return 1
    if 'molecular' in f:
        return 1
    return 0

targets = [
    'vital_status',
    'cancer_type',
    'stage',
    'metastasis',
    'treatment_outcome',
    'treatment_type',
    'clinical_trial',
    'age_at_index',
    'classification_of_tumor',
    'disease_response',
    'tissue_or_organ_of_origin',
]

output_dir = 'frontend/public/'
os.makedirs(output_dir, exist_ok=True)

for target in targets:
    try:
        features = joblib.load(f'feature_names_{target}.joblib')
        example_row = [get_realistic_value(f) for f in features]
        with open(os.path.join(output_dir, f'batch_template_{target}.csv'), 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(features)
            writer.writerow(example_row)
        print(f'Wrote batch_template_{target}.csv with {len(features)} columns.')
    except Exception as e:
        print(f'ERROR for {target}: {e}') 