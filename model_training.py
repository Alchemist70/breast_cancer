import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, mean_squared_error, r2_score, accuracy_score
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import joblib
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Updated targets list to include vital_status, stage, and new targets
targets = [
    'vital_status',  # Survival prediction
    'cancer_type',   # Cancer subtype classification
    'stage',         # AJCC pathologic stage
    'metastasis',    # Metastasis at diagnosis
    'treatment_outcome',  # Treatment response
    'treatment_type',     # Treatment modality
    'clinical_trial',     # Clinical trial participation
    'age_at_index',       # Age-based risk stratification
    'classification_of_tumor',  # Primary vs Metastasis classification
    'disease_response',         # Treatment response prediction
    'tissue_or_organ_of_origin',  # Tumor origin classification
    'malignancy',         # Legacy target
    'tissue_change',      # Tissue changes
    'prognosis',          # Prognosis prediction
    'therapy',            # Therapy recommendation
    'genetic_cause'       # Genetic cause identification
]

def advanced_feature_selection(X, y, n_features=100):
    """Advanced feature selection using multiple methods"""
    print(f"   Performing advanced feature selection...")
    
    # Method 1: Statistical feature selection
    selector1 = SelectKBest(score_func=f_classif, k=min(n_features, X.shape[1]))
    X_selected1 = selector1.fit_transform(X, y)
    selected_features1 = X.columns[selector1.get_support()].tolist()
    
    # Method 2: Recursive feature elimination with Random Forest
    rf_for_rfe = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    selector2 = RFE(estimator=rf_for_rfe, n_features_to_select=min(n_features, X.shape[1]))
    X_selected2 = selector2.fit_transform(X, y)
    selected_features2 = X.columns[selector2.get_support()].tolist()
    
    # Combine features from both methods
    combined_features = list(set(selected_features1 + selected_features2))
    print(f"   Selected {len(combined_features)} features from {X.shape[1]} original features")
    
    return X[combined_features], combined_features

def create_ensemble_model(is_classification=True, n_jobs=-1):
    """Create an advanced ensemble model"""
    if is_classification:
        # Create base models with optimized parameters
        rf1 = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=5, 
                                   min_samples_leaf=2, random_state=42, n_jobs=n_jobs)
        rf2 = RandomForestClassifier(n_estimators=300, max_depth=20, min_samples_split=3, 
                                   min_samples_leaf=1, random_state=43, n_jobs=n_jobs)
        gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=8, 
                                      random_state=44)
        et = ExtraTreesClassifier(n_estimators=200, max_depth=15, random_state=45, n_jobs=n_jobs)
        
        # Create voting classifier with soft voting
        ensemble = VotingClassifier(
            estimators=[
                ('rf1', rf1), ('rf2', rf2), ('gb', gb), ('et', et)
            ],
            voting='soft'
        )
    else:
        # For regression, use simpler ensemble
        rf1 = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=n_jobs)
        rf2 = RandomForestRegressor(n_estimators=300, max_depth=20, random_state=43, n_jobs=n_jobs)
        
        ensemble = VotingClassifier(
            estimators=[('rf1', rf1), ('rf2', rf2)],
            voting='soft'
        )
    
    return ensemble

def optimize_hyperparameters(X, y, is_classification=True):
    """Optimize hyperparameters using GridSearchCV"""
    print(f"   Optimizing hyperparameters...")
    
    if is_classification:
        # Define parameter grid for Random Forest
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None]
        }
        
        # Use Random Forest for optimization
        base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        
        # Perform grid search with cross-validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid_search = GridSearchCV(
            base_model, param_grid, cv=cv, scoring='accuracy', 
            n_jobs=-1, verbose=0
        )
        grid_search.fit(X, y)
        
        print(f"   Best parameters: {grid_search.best_params_}")
        print(f"   Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    else:
        # For regression
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        base_model = RandomForestRegressor(random_state=42, n_jobs=-1)
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        grid_search = GridSearchCV(
            base_model, param_grid, cv=cv, scoring='r2', 
            n_jobs=-1, verbose=0
        )
        grid_search.fit(X, y)
        
        print(f"   Best parameters: {grid_search.best_params_}")
        print(f"   Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_

def advanced_preprocessing(X, y):
    """Advanced preprocessing techniques"""
    print(f"   Performing advanced preprocessing...")
    
    # Handle outliers using IQR method
    for col in X.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = X[col].quantile(0.25)
        Q3 = X[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap outliers instead of removing them
        X[col] = np.where(X[col] < lower_bound, lower_bound, X[col])
        X[col] = np.where(X[col] > upper_bound, upper_bound, X[col])
    
    # Advanced missing value imputation
    for col in X.select_dtypes(include=['float64', 'int64']).columns:
        if X[col].isnull().sum() > 0:
            # Use median for numerical features
            X[col] = X[col].fillna(X[col].median())
    
    for col in X.select_dtypes(include=['object']).columns:
        if X[col].isnull().sum() > 0:
            # Use mode for categorical features
            mode_val = X[col].mode()[0] if len(X[col].mode()) > 0 else 'Unknown'
            X[col] = X[col].fillna(mode_val)
    
    return X

for target in targets:
    data_file = f'ml_data_{target}.csv'
    if not os.path.exists(data_file):
        print(f"❌ {data_file} not found, skipping {target}.")
        continue
    
    print(f'📥 Loading {data_file}...')
    df = pd.read_csv(data_file)
    
    if target not in df.columns:
        print(f"❌ Target column '{target}' not found in {data_file}, skipping.")
        continue
    
    print(f"   Dataset shape: {df.shape}")
    print(f"   Target distribution: {df[target].value_counts()}")
    
    X = df.drop([target], axis=1)
    y = df[target]
    
    # Drop rows with missing target
    mask = ~pd.isnull(y)
    X = X[mask]
    y = y[mask]
    
    print(f"   After removing missing targets: {X.shape}")
    
    # Advanced preprocessing
    X = advanced_preprocessing(X, y)
    
    # Encode categorical features
    for col in X.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))

    # Final NaN fill to ensure no missing values remain
    X = X.fillna(0)
    
    # Encode target if classification
    is_classification = True
    if target == 'prognosis' and len(np.unique(y)) > 10:
        is_classification = False
    
    if is_classification and y.dtype == 'object':
        le_y = LabelEncoder()
        y = le_y.fit_transform(y.astype(str))
        print(f"   Encoded target classes: {le_y.classes_}")
    
    # Advanced feature selection
    X, selected_features = advanced_feature_selection(X, y, n_features=min(200, X.shape[1]))
    
    # Split with stratification for classification
    if is_classification:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    print(f"   Training set: {X_train.shape}, Test set: {X_test.shape}")
    
    # Advanced scaling with RobustScaler (more robust to outliers)
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Hyperparameter optimization
    optimized_model = optimize_hyperparameters(X_train_scaled, y_train, is_classification)
    
    # Create ensemble model
    ensemble_model = create_ensemble_model(is_classification)
    
    print(f"   Training optimized model...")
    optimized_model.fit(X_train_scaled, y_train)
    
    print(f"   Training ensemble model...")
    ensemble_model.fit(X_train_scaled, y_train)
    
    # Evaluate both models
    if is_classification:
        # Optimized model evaluation
        y_pred_opt = optimized_model.predict(X_test_scaled)
        y_proba_opt = optimized_model.predict_proba(X_test_scaled) if hasattr(optimized_model, 'predict_proba') else None
        report_opt = classification_report(y_test, y_pred_opt, output_dict=True)
        cm_opt = confusion_matrix(y_test, y_pred_opt).tolist()
        
        # Ensemble model evaluation
        y_pred_ens = ensemble_model.predict(X_test_scaled)
        y_proba_ens = ensemble_model.predict_proba(X_test_scaled) if hasattr(ensemble_model, 'predict_proba') else None
        report_ens = classification_report(y_test, y_pred_ens, output_dict=True)
        cm_ens = confusion_matrix(y_test, y_pred_ens).tolist()
        
        # Calculate ROC AUC
        try:
            if y_proba_opt is not None and len(np.unique(y_test)) > 2:
                roc_opt = roc_auc_score(y_test, y_proba_opt, multi_class='ovr', average='macro')
            elif y_proba_opt is not None:
                roc_opt = roc_auc_score(y_test, y_proba_opt[:,1])
            else:
                roc_opt = None
        except Exception as e:
            roc_opt = str(e)
        
        try:
            if y_proba_ens is not None and len(np.unique(y_test)) > 2:
                roc_ens = roc_auc_score(y_test, y_proba_ens, multi_class='ovr', average='macro')
            elif y_proba_ens is not None:
                roc_ens = roc_auc_score(y_test, y_proba_ens[:,1])
            else:
                roc_ens = None
        except Exception as e:
            roc_ens = str(e)
        
        print(f'✅ {target} classification report (Optimized Model):')
        print(classification_report(y_test, y_pred_opt))
        print(f'   ROC AUC: {roc_opt}')
        
        print(f'✅ {target} classification report (Ensemble Model):')
        print(classification_report(y_test, y_pred_ens))
        print(f'   ROC AUC: {roc_ens}')
        
        # Choose the better model based on accuracy
        acc_opt = report_opt['accuracy']
        acc_ens = report_ens['accuracy']
        
        if acc_ens > acc_opt:
            final_model = ensemble_model
            final_report = report_ens
            final_cm = cm_ens
            final_roc = roc_ens
            model_type = "Ensemble"
        else:
            final_model = optimized_model
            final_report = report_opt
            final_cm = cm_opt
            final_roc = roc_opt
            model_type = "Optimized"
        
        print(f"   Selected {model_type} model with accuracy: {max(acc_opt, acc_ens):.4f}")
        
    else:
        # Regression evaluation
        y_pred_opt = optimized_model.predict(X_test_scaled)
        mse_opt = mean_squared_error(y_test, y_pred_opt)
        r2_opt = r2_score(y_test, y_pred_opt)
        
        y_pred_ens = ensemble_model.predict(X_test_scaled)
        mse_ens = mean_squared_error(y_test, y_pred_ens)
        r2_ens = r2_score(y_test, y_pred_ens)
        
        print(f'✅ {target} regression (Optimized Model) MSE: {mse_opt:.4f}, R2: {r2_opt:.4f}')
        print(f'✅ {target} regression (Ensemble Model) MSE: {mse_ens:.4f}, R2: {r2_ens:.4f}')
        
        # Choose the better model based on R2
        if r2_ens > r2_opt:
            final_model = ensemble_model
            mse = mse_ens
            r2 = r2_ens
            model_type = "Ensemble"
        else:
            final_model = optimized_model
            mse = mse_opt
            r2 = r2_opt
            model_type = "Optimized"
        
        print(f"   Selected {model_type} model with R2: {max(r2_opt, r2_ens):.4f}")
    
    # Save model, scaler, summary
    joblib.dump(final_model, f'{target}_enhanced_model.joblib')
    joblib.dump(scaler, f'scaler_{target}.joblib')
    
    # Save feature names for later use
    joblib.dump(selected_features, f'feature_names_{target}.joblib')
    
    summary = {
        'target': target,
        'n_samples': len(df),
        'n_features': X.shape[1],
        'selected_features': len(selected_features),
        'model': type(final_model).__name__,
        'model_type': model_type,
        'is_classification': is_classification,
        'feature_names': selected_features
    }
    
    if is_classification:
        summary['classification_report'] = final_report
        summary['confusion_matrix'] = final_cm
        summary['roc_auc'] = final_roc
        if hasattr(le_y, 'classes_'):
            summary['target_classes'] = le_y.classes_.tolist()
    else:
        summary['mse'] = mse
        summary['r2'] = r2
    
    with open(f'model_summary_{target}.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f'💾 Saved enhanced model, scaler, and summary for {target}.')
    print('=' * 50) 