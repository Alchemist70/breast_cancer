import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class MemoryEfficientTCGAPipeline:
    """
    Memory-efficient data pipeline for TCGA Breast Cancer data processing
    """
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
        self.processed_data = {}
        
    def analyze_data_structure(self):
        """Analyze data structure without loading full datasets"""
        print("🔍 Analyzing data structure...")
        
        analysis = {}
        data_files = {
            'clinical': 'clinical.tsv',
            'pathology_detail': 'pathology_detail.tsv',
            'sample': 'sample.tsv',
            'follow_up': 'follow_up.tsv',
            'exposure': 'exposure.tsv',
            'aliquot': 'aliquot.tsv',
            'analyte': 'analyte.tsv',
            'portion': 'portion.tsv',
            'slide': 'slide.tsv'
        }
        
        for name, filename in data_files.items():
            file_path = self.data_dir / filename
            if file_path.exists():
                try:
                    # Read only header to get column names
                    header = pd.read_csv(file_path, sep='\t', nrows=0)
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    
                    analysis[name] = {
                        'columns': header.columns.tolist(),
                        'file_size_mb': round(file_size, 2),
                        'file_path': str(file_path)
                    }
                    
                    print(f"   📊 {name}: {len(header.columns)} columns, {file_size:.1f}MB")
                    
                except Exception as e:
                    print(f"   ❌ Error analyzing {name}: {str(e)}")
        
        return analysis
    
    def process_clinical_data(self):
        """Process clinical data - the most important dataset"""
        print("📋 Processing clinical data...")
        
        try:
            # Load clinical data in chunks
            clinical_file = self.data_dir / 'clinical.tsv'
            if not clinical_file.exists():
                print("❌ Clinical data file not found!")
                return pd.DataFrame()
            
            # Read in chunks to avoid memory issues
            chunks = []
            chunk_size = 500  # Smaller chunks for memory efficiency
            
            for chunk in pd.read_csv(clinical_file, sep='\t', chunksize=chunk_size):
                # Clean chunk
                chunk = chunk.fillna('Unknown')
                chunks.append(chunk)
            
            clinical_df = pd.concat(chunks, ignore_index=True)
            
            # Convert object columns to category for memory efficiency
            for col in clinical_df.select_dtypes(include=['object']).columns:
                if clinical_df[col].nunique() < len(clinical_df) * 0.5:  # Only if cardinality is reasonable
                    clinical_df[col] = clinical_df[col].astype('category')
            
            print(f"   ✅ Processed {len(clinical_df)} clinical records")
            return clinical_df
            
        except Exception as e:
            print(f"   ❌ Error processing clinical data: {str(e)}")
            return pd.DataFrame()
    
    def process_pathology_data(self):
        """Process pathology data"""
        print("🔬 Processing pathology data...")
        
        try:
            pathology_file = self.data_dir / 'pathology_detail.tsv'
            if not pathology_file.exists():
                print("❌ Pathology data file not found!")
                return pd.DataFrame()
            
            pathology_df = pd.read_csv(pathology_file, sep='\t')
            pathology_df = pathology_df.fillna('Unknown')
            
            # Convert to categories for memory efficiency
            for col in pathology_df.select_dtypes(include=['object']).columns:
                if pathology_df[col].nunique() < len(pathology_df) * 0.5:
                    pathology_df[col] = pathology_df[col].astype('category')
            
            print(f"   ✅ Processed {len(pathology_df)} pathology records")
            return pathology_df
            
        except Exception as e:
            print(f"   ❌ Error processing pathology data: {str(e)}")
            return pd.DataFrame()
    
    def extract_target_variables(self, clinical_df: pd.DataFrame, pathology_df: pd.DataFrame):
        """Extract target variables for ML models"""
        print("🎯 Extracting target variables...")
        
        targets = {}
        
        # 1. Malignancy (Benign vs Malignant)
        malignancy_cols = []
        for col in clinical_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['malignant', 'benign', 'tumor_type']):
                malignancy_cols.append(col)
        
        if malignancy_cols:
            targets['malignancy'] = clinical_df[malignancy_cols[0]]  # Use first available
            print(f"   ✅ Malignancy target: {malignancy_cols[0]}")
        
        # 2. Cancer Type
        cancer_type_cols = []
        for col in clinical_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['classification', 'subtype', 'histology']):
                cancer_type_cols.append(col)
        
        if cancer_type_cols:
            targets['cancer_type'] = clinical_df[cancer_type_cols[0]]
            print(f"   ✅ Cancer type target: {cancer_type_cols[0]}")
        
        # 3. Metastasis
        metastasis_cols = []
        for col in clinical_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['metastasis', 'metastatic', 'lymph_node']):
                metastasis_cols.append(col)
        
        if metastasis_cols:
            targets['metastasis'] = clinical_df[metastasis_cols[0]]
            print(f"   ✅ Metastasis target: {metastasis_cols[0]}")
        
        # 4. Tissue Changes (from pathology data)
        tissue_change_cols = []
        if not pathology_df.empty:
            for col in pathology_df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['dysplasia', 'hyperplasia', 'carcinoma']):
                    tissue_change_cols.append(col)
        
        if tissue_change_cols:
            targets['tissue_change'] = pathology_df[tissue_change_cols[0]]
            print(f"   ✅ Tissue change target: {tissue_change_cols[0]}")
        
        # 5. Prognosis
        prognosis_cols = []
        for col in clinical_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['survival', 'outcome', 'prognosis']):
                prognosis_cols.append(col)
        
        if prognosis_cols:
            targets['prognosis'] = clinical_df[prognosis_cols[0]]
            print(f"   ✅ Prognosis target: {prognosis_cols[0]}")
        
        return targets
    
    def extract_features(self, clinical_df: pd.DataFrame, pathology_df: pd.DataFrame):
        """Extract feature columns for ML models"""
        print("🔍 Extracting features...")
        
        features = {}
        
        # Demographic features
        demographic_cols = []
        for col in clinical_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['age', 'gender', 'race', 'ethnicity', 'height', 'weight']):
                demographic_cols.append(col)
        
        if demographic_cols:
            features['demographic'] = clinical_df[demographic_cols]
            print(f"   ✅ Extracted {len(demographic_cols)} demographic features")
        
        # Clinical features
        clinical_feature_cols = []
        for col in clinical_df.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['diagnosis', 'stage', 'grade', 'treatment']):
                clinical_feature_cols.append(col)
        
        if clinical_feature_cols:
            features['clinical'] = clinical_df[clinical_feature_cols]
            print(f"   ✅ Extracted {len(clinical_feature_cols)} clinical features")
        
        # Pathological features
        if not pathology_df.empty:
            pathological_cols = pathology_df.columns.tolist()
            features['pathological'] = pathology_df[pathological_cols]
            print(f"   ✅ Extracted {len(pathological_cols)} pathological features")
        
        return features
    
    def prepare_ml_dataset(self, clinical_df: pd.DataFrame, pathology_df: pd.DataFrame, targets: Dict):
        """Prepare final ML dataset"""
        print("🤖 Preparing ML dataset...")
        
        # Start with clinical data as base
        ml_df = clinical_df.copy()
        
        # Add pathology data if available
        if not pathology_df.empty:
            # Find common identifier
            common_cols = set(clinical_df.columns) & set(pathology_df.columns)
            if common_cols:
                merge_col = list(common_cols)[0]
                ml_df = ml_df.merge(pathology_df, on=merge_col, how='left', suffixes=('', '_pathology'))
                print(f"   ✅ Merged pathology data using '{merge_col}'")
        
        # Handle missing values for categorical columns
        categorical_cols = ml_df.select_dtypes(include=['category']).columns
        for col in categorical_cols:
            # Add 'Unknown' to categories if not present
            if 'Unknown' not in ml_df[col].cat.categories:
                ml_df[col] = ml_df[col].cat.add_categories(['Unknown'])
            ml_df[col] = ml_df[col].fillna('Unknown')
        
        # Handle missing values for object columns
        object_cols = ml_df.select_dtypes(include=['object']).columns
        for col in object_cols:
            ml_df[col] = ml_df[col].fillna('Unknown')
        
        # Convert categorical variables to numeric
        all_categorical_cols = ml_df.select_dtypes(include=['object', 'category']).columns
        for col in all_categorical_cols:
            ml_df[col] = pd.Categorical(ml_df[col]).codes
        
        # Convert numeric columns
        numeric_cols = ml_df.select_dtypes(include=['object']).columns
        for col in numeric_cols:
            try:
                ml_df[col] = pd.to_numeric(ml_df[col], errors='coerce')
            except:
                pass
        
        # Fill NaN values in numeric columns
        ml_df = ml_df.fillna(0)
        
        print(f"   ✅ Final ML dataset shape: {ml_df.shape}")
        return ml_df
    
    def run_pipeline(self):
        """Run the complete memory-efficient pipeline"""
        print("🚀 Starting Memory-Efficient TCGA Breast Cancer Pipeline")
        print("=" * 65)
        
        # Analyze data structure
        analysis = self.analyze_data_structure()
        
        # Process main datasets
        clinical_df = self.process_clinical_data()
        pathology_df = self.process_pathology_data()
        
        if clinical_df.empty:
            print("❌ No clinical data available!")
            return None, None
        
        # Extract targets and features
        targets = self.extract_target_variables(clinical_df, pathology_df)
        features = self.extract_features(clinical_df, pathology_df)
        
        # Prepare ML dataset
        ml_dataset = self.prepare_ml_dataset(clinical_df, pathology_df, targets)
        
        # Save results
        ml_dataset.to_csv('breast_cancer_ml_data.csv', index=False)
        print("💾 Saved ML dataset to 'breast_cancer_ml_data.csv'")
        
        # Save targets separately
        target_data = {}
        for target_name, target_series in targets.items():
            if not target_series.empty:
                target_data[target_name] = target_series.values
        
        with open('target_variables.json', 'w') as f:
            json.dump({k: v.tolist() if hasattr(v, 'tolist') else v for k, v in target_data.items()}, f)
        
        print("💾 Saved target variables to 'target_variables.json'")
        
        # Print summary
        print(f"\n✅ Pipeline completed successfully!")
        print(f"📊 Dataset shape: {ml_dataset.shape}")
        print(f"🎯 Available targets: {list(targets.keys())}")
        print(f"🔍 Available features: {list(features.keys())}")
        
        return ml_dataset, targets

if __name__ == "__main__":
    pipeline = MemoryEfficientTCGAPipeline()
    ml_data, targets = pipeline.run_pipeline() 