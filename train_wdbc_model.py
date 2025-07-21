import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import re

# Load the dataset first to get the number of columns
df = pd.read_csv('wdbc.data', header=None)

# Generate feature names based on the structure described in wdbc.names
base_features = [
    'radius', 'texture', 'perimeter', 'area', 'smoothness',
    'compactness', 'concavity', 'concave points', 'symmetry', 'fractal dimension'
]
suffixes = ['_mean', '_se', '_worst']
feature_names = ['id', 'diagnosis']
for suffix in suffixes:
    for feature in base_features:
        feature_names.append(feature.replace(' ', '_') + suffix)

# Ensure the number of generated names matches the number of columns
if len(feature_names) != df.shape[1]:
    raise ValueError(f"Generated {len(feature_names)} feature names, but data has {df.shape[1]} columns.")

df.columns = feature_names

# Prepare data
X = df.drop(['id', 'diagnosis'], axis=1)
y = df['diagnosis'].apply(lambda x: 1 if x == 'M' else 0)  # Malignant=1, Benign=0

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = model.predict(X_test_scaled)
print("WDBC Malignancy Model Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Benign', 'Malignant']))

# Save the model, scaler, and feature names
joblib.dump(model, 'wdbc_malignancy_model.joblib')
joblib.dump(scaler, 'wdbc_malignancy_scaler.joblib')
joblib.dump(list(X.columns), 'wdbc_malignancy_features.joblib')

print("\nWDBC malignancy model, scaler, and feature list saved successfully.") 