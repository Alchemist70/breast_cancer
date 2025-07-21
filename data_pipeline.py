import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class TCGA_BreastCancerPipeline:
    """
    Comprehensive data pipeline for TCGA Breast Cancer data processing
    """
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
        self.processed_data = {}
        self.feature_columns = {}
        self.target_columns = {}
        
    def load_and_clean_data(self) -> Dict[str, pd.DataFrame]:
        """Load and perform initial cleaning of all TSV files"""
        print("🔄 Loading and cleaning TCGA data...")
        
        data_files = {
            'clinical': 'clinical.tsv',
            'pathology': 'pathology_detail.tsv', 
            'sample': 'sample.tsv',
            'follow_up': 'follow_up.tsv',
            'exposure': 'exposure.tsv',
            'family_history': 'family_history.tsv',
            'aliquot': 'aliquot.tsv',
            'analyte': 'analyte.tsv',
            'portion': 'portion.tsv',
            'slide': 'slide.tsv'
        }
        
        cleaned_data = {}
        
        for name, file_path in data_files.items():
            if os.path.exists(file_path):
                print(f"📊 Processing {name} data...")
                try:
                    df = pd.read_csv(file_path, sep='\t', low_memory=False)
                    df = self._clean_dataframe(df, name)
                    cleaned_data[name] = df
                    print(f"   ✅ Loaded {df.shape[0]} rows, {df.shape[1]} columns")
                except Exception as e:
                    print(f"   ❌ Error loading {name}: {e}")
            else:
                print(f"   ⚠️ File not found: {file_path}")
        
        self.processed_data = cleaned_data
        return cleaned_data
    
    def _clean_dataframe(self, df: pd.DataFrame, name: str) -> pd.DataFrame:
        """Clean individual dataframe"""
        # Remove completely empty columns
        df = df.dropna(axis=1, how='all')
        
        # Replace '--' with NaN
        df = df.replace("'--", np.nan)
        df = df.replace("--", np.nan)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        return df
    
    def extract_target_variables(self, unified_df: pd.DataFrame) -> Dict[str, pd.Series]:
        """Extract target variables for different prediction tasks."""
        print("🎯 Extracting target variables...")
        targets = {}
        
        # Vital status (Alive/Dead)
        if 'demographic.vital_status' in unified_df.columns:
            vs = unified_df['demographic.vital_status']
            valid_mask = vs.isin(['Alive', 'Dead'])
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid vital_status values (Alive/Dead)")
                targets['vital_status'] = vs.where(valid_mask)
        
        # Cancer type (primary diagnosis)
        if 'diagnoses.primary_diagnosis' in unified_df.columns:
            ct = unified_df['diagnoses.primary_diagnosis']
            valid_mask = (ct != 'Not Reported') & (ct != "'--") & ct.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid cancer_type values")
                targets['cancer_type'] = ct.where(valid_mask)
        
        # Stage (AJCC pathologic stage)
        if 'diagnoses.ajcc_pathologic_stage' in unified_df.columns:
            st = unified_df['diagnoses.ajcc_pathologic_stage']
            valid_mask = (st != 'Not Reported') & (st != "'--") & st.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid stage values")
                targets['stage'] = st.where(valid_mask)
        
        # Metastasis at diagnosis
        if 'diagnoses.metastasis_at_diagnosis' in unified_df.columns:
            mt = unified_df['diagnoses.metastasis_at_diagnosis']
            valid_mask = (mt != "'--") & mt.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid metastasis values")
                targets['metastasis'] = mt.where(valid_mask)
        
        # Tumor grade
        if 'diagnoses.tumor_grade' in unified_df.columns:
            tg = unified_df['diagnoses.tumor_grade']
            valid_mask = (tg != "'--") & tg.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid tumor_grade values")
                targets['tumor_grade'] = tg.where(valid_mask)
        
        # Treatment outcome
        if 'treatments.treatment_outcome' in unified_df.columns:
            to = unified_df['treatments.treatment_outcome']
            valid_mask = (to != "'--") & (to != 'Not Reported') & to.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid treatment_outcome values")
                targets['treatment_outcome'] = to.where(valid_mask)
        
        # Treatment type
        if 'treatments.treatment_type' in unified_df.columns:
            tt = unified_df['treatments.treatment_type']
            valid_mask = (tt != "'--") & tt.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid treatment_type values")
                targets['treatment_type'] = tt.where(valid_mask)
        
        # Clinical trial participation
        if 'treatments.clinical_trial_indicator' in unified_df.columns:
            ct = unified_df['treatments.clinical_trial_indicator']
            valid_mask = (ct != "'--") & ct.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid clinical_trial values")
                targets['clinical_trial'] = ct.where(valid_mask)
        
        # Age at diagnosis (for age-based risk stratification)
        if 'demographic.age_at_index' in unified_df.columns:
            age = unified_df['demographic.age_at_index']
            valid_mask = (age != "'--") & age.notnull() & pd.to_numeric(age, errors='coerce').notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid age_at_index values")
                targets['age_at_index'] = age.where(valid_mask)
        
        # Tumor classification (Primary vs Metastasis)
        if 'diagnoses.classification_of_tumor' in unified_df.columns:
            tc = unified_df['diagnoses.classification_of_tumor']
            valid_mask = (tc != "'--") & (tc != 'Not Reported') & tc.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid classification_of_tumor values")
                targets['classification_of_tumor'] = tc.where(valid_mask)
        
        # Disease response (from follow-up data)
        if 'follow_ups.disease_response' in unified_df.columns:
            dr = unified_df['follow_ups.disease_response']
            valid_mask = (dr != "'--") & (dr != 'Not Reported') & dr.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid disease_response values")
                targets['disease_response'] = dr.where(valid_mask)
        
        # Tissue/organ of origin
        if 'diagnoses.tissue_or_organ_of_origin' in unified_df.columns:
            to = unified_df['diagnoses.tissue_or_organ_of_origin']
            valid_mask = (to != "'--") & (to != 'Not Reported') & to.notnull()
            if valid_mask.sum() > 0:
                print(f"   Found {valid_mask.sum()} valid tissue_or_organ_of_origin values")
                targets['tissue_or_organ_of_origin'] = to.where(valid_mask)
        
        print(f"   ✅ Extracted {len(targets)} targets with data")
        return targets
    
    def extract_features(self) -> Dict[str, pd.DataFrame]:
        """Extract features for AI model training"""
        print("\n🔍 Extracting features...")
        
        features = {}
        
        # Clinical features
        if 'clinical' in self.processed_data:
            clin_df = self.processed_data['clinical']
            
            # Demographic features
            demo_cols = [col for col in clin_df.columns if any(term in col.lower() 
                        for term in ['age', 'gender', 'race', 'ethnicity', 'demographic'])]
            
            if demo_cols:
                features['demographics'] = clin_df[demo_cols]
                print(f"   Extracted {len(demo_cols)} demographic features")
        
        # Pathology features
        if 'pathology' in self.processed_data:
            path_df = self.processed_data['pathology']
            
            # Tumor characteristics
            tumor_cols = [col for col in path_df.columns if any(term in col.lower() 
                         for term in ['tumor', 'size', 'grade', 'stage', 'margin', 'invasion'])]
            
            if tumor_cols:
                features['tumor_characteristics'] = path_df[tumor_cols]
                print(f"   Extracted {len(tumor_cols)} tumor characteristic features")
        
        # Genomic features (from analyte data)
        if 'analyte' in self.processed_data:
            analyte_df = self.processed_data['analyte']
            
            # Quality metrics
            quality_cols = [col for col in analyte_df.columns if any(term in col.lower() 
                           for term in ['ratio', 'concentration', 'integrity', 'quality'])]
            
            if quality_cols:
                features['genomic_quality'] = analyte_df[quality_cols]
                print(f"   Extracted {len(quality_cols)} genomic quality features")
        
        # Exposure features
        if 'exposure' in self.processed_data:
            exp_df = self.processed_data['exposure']
            if not exp_df.empty:
                features['exposure'] = exp_df
                print(f"   Extracted {exp_df.shape[1]} exposure features")
        
        # Family history features
        if 'family_history' in self.processed_data:
            fam_df = self.processed_data['family_history']
            if not fam_df.empty:
                features['family_history'] = fam_df
                print(f"   Extracted {fam_df.shape[1]} family history features")
        
        self.feature_columns = features
        return features
    
    def create_unified_dataset(self):
        """Create a unified dataset from all processed data sources."""
        print("🔗 Creating unified dataset...")
        
        # Start with clinical data as base
        if 'clinical' in self.processed_data:
            unified_df = self.processed_data['clinical'].copy()
            print(f"   Starting with clinical data: {unified_df.shape}")
        else:
            print("   ⚠️ No clinical data found, starting with empty DataFrame")
            unified_df = pd.DataFrame()
        
        # Merge pathology data (smaller, more relevant)
        if 'pathology' in self.processed_data:
            path_df = self.processed_data['pathology']
            if not unified_df.empty:
                # Use left merge to keep only clinical cases that have pathology data
                unified_df = unified_df.merge(path_df, on='cases.submitter_id', how='inner')
                print(f"   Merged pathology data: {unified_df.shape}")
            else:
                unified_df = path_df
                print(f"   Using pathology data as base: {unified_df.shape}")
        
        # Merge sample data (smaller dataset)
        if 'sample' in self.processed_data and not unified_df.empty:
            sample_df = self.processed_data['sample']
            unified_df = unified_df.merge(sample_df, on='cases.submitter_id', how='left')
            print(f"   Merged sample data: {unified_df.shape}")
        
        # Merge follow-up data (take only the first follow-up per patient to reduce size)
        if 'follow_up' in self.processed_data and not unified_df.empty:
            follow_df = self.processed_data['follow_up']
            # Take only the first follow-up per patient to reduce size
            follow_df = follow_df.groupby('cases.submitter_id').first().reset_index()
            
            # Handle duplicate columns by dropping them from follow_df
            join_key = 'cases.submitter_id'
            follow_df = follow_df[[col for col in follow_df.columns if col not in unified_df.columns or col == join_key]]
            
            unified_df = unified_df.merge(follow_df, on='cases.submitter_id', how='left')
            print(f"   Merged follow-up data (reduced): {unified_df.shape}")
        
        # Merge exposure data (small dataset)
        if 'exposure' in self.processed_data and not unified_df.empty:
            exp_df = self.processed_data['exposure']
            # Drop columns from exp_df that are already in unified_df, except join key
            join_key = 'cases.submitter_id'
            exp_df = exp_df[[col for col in exp_df.columns if col not in unified_df.columns or col == join_key]]
            unified_df = unified_df.merge(exp_df, on=join_key, how='left')
            print(f"   Merged exposure data: {unified_df.shape}")
        
        print(f"   ✅ Final unified dataset: {unified_df.shape}")
        return unified_df
    
    def prepare_for_ml(self, unified_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, pd.Series]]:
        """Prepare data for machine learning with memory-efficient processing."""
        print("🤖 Preparing data for machine learning...")
        
        # Only process targets that have actual data
        targets = self.extract_target_variables(unified_df)
        if not targets:
            print("   ⚠️ No targets with data found, creating dummy target for testing")
            targets['therapy'] = pd.Series(['No'] * len(unified_df), index=unified_df.index)
        
        print(f"   Processing {len(targets)} targets: {list(targets.keys())}")
        
        # Memory-efficient processing
        print("   Handling missing values...")
        # Fill missing values with appropriate defaults
        for col in unified_df.columns:
            if unified_df[col].dtype == 'object':
                unified_df[col] = unified_df[col].fillna('Unknown')
            else:
                unified_df[col] = unified_df[col].fillna(unified_df[col].median())
        
        print("   Encoding categorical variables...")
        # Only encode categorical columns to save memory
        categorical_cols = unified_df.select_dtypes(include=['object']).columns
        print(f"   Found {len(categorical_cols)} categorical columns")
        
        # Use LabelEncoder for memory efficiency
        from sklearn.preprocessing import LabelEncoder
        label_encoders = {}
        
        for col in categorical_cols:
            if col in unified_df.columns:
                le = LabelEncoder()
                # Handle missing values in encoding
                col_data = unified_df[col].fillna('Unknown')
                unified_df[col] = le.fit_transform(col_data)
                label_encoders[col] = le
        
        # Save encoders for later use
        self.label_encoders = label_encoders
        
        print(f"   ✅ Final ML-ready dataset: {unified_df.shape}")
        return unified_df, targets
    
    def save_processed_data(self, output_dir: str = "processed_data"):
        """Save processed data to files"""
        print(f"\n💾 Saving processed data to {output_dir}...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save individual datasets
        for name, df in self.processed_data.items():
            df.to_csv(f"{output_dir}/{name}_processed.csv", index=False)
        
        # Save unified dataset
        if hasattr(self, 'unified_dataset'):
            self.unified_dataset.to_csv(f"{output_dir}/unified_dataset.csv", index=False)
        
        # Save feature and target information
        with open(f"{output_dir}/data_info.json", 'w') as f:
            info = {
                'feature_columns': {k: list(v.columns) for k, v in self.feature_columns.items()},
                'target_columns': {k: str(type(v)) for k, v in self.target_columns.items()},
                'dataset_sizes': {k: v.shape for k, v in self.processed_data.items()}
            }
            json.dump(info, f, indent=2, default=str)
        
        print(f"   ✅ Data saved to {output_dir}/")
    
    def save_ml_datasets_for_targets(self, ml_ready_df: pd.DataFrame, targets: Dict[str, pd.Series]):
        """Save separate ML-ready datasets for each target."""
        print("💾 Saving ML-ready datasets for each target...")
        
        for target_name, target_series in targets.items():
            if target_series is not None and len(target_series) > 0:
                print(f"   Processing target: {target_name}")
                
                # Create dataset for this target
                target_df = ml_ready_df.copy()
                
                # Add target column
                target_df[target_name] = target_series
                
                # Remove rows where target is missing
                target_df = target_df.dropna(subset=[target_name])
                
                if len(target_df) > 0:
                    # Save to CSV
                    filename = f"ml_data_{target_name}.csv"
                    target_df.to_csv(filename, index=False)
                    print(f"      ✅ Saved {len(target_df)} rows to {filename}")
                else:
                    print(f"      ⚠️ No data for target {target_name} after removing missing values")
            else:
                print(f"   ⚠️ Skipping target {target_name} - no data")
        
        print("   ✅ ML datasets saved successfully")
    
    def run_pipeline(self) -> Tuple[pd.DataFrame, Dict[str, pd.Series]]:
        """Run the complete data pipeline"""
        print("🚀 Starting TCGA Breast Cancer Data Pipeline")
        print("=" * 60)
        
        # Step 1: Load and clean data
        self.load_and_clean_data()
        
        # Step 2: Extract target variables
        unified_df = self.create_unified_dataset() # Create unified_df here
        targets = self.extract_target_variables(unified_df)
        
        # Step 3: Extract features
        self.extract_features()
        
        # Step 4: Create unified dataset
        self.unified_dataset = unified_df
        
        # Step 5: Prepare for ML
        ml_ready_df, targets_final = self.prepare_for_ml(unified_df)
        
        # Step 6: Save processed data for each target
        self.save_ml_datasets_for_targets(ml_ready_df, targets)
        
        print("\n✅ Pipeline completed successfully!")
        print(f"Final dataset shape: {ml_ready_df.shape}")
        print(f"Number of targets: {len(targets)}")
        
        return ml_ready_df, targets

if __name__ == "__main__":
    # Run the pipeline
    pipeline = TCGA_BreastCancerPipeline()
    ml_data, targets = pipeline.run_pipeline()
    
    print(f"\n📊 Final Dataset Summary:")
    print(f"   Features: {ml_data.shape[1]}")
    print(f"   Samples: {ml_data.shape[0]}")
    print(f"   Targets: {list(targets.keys())}") 