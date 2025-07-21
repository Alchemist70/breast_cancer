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
    Memory-optimized data pipeline for TCGA Breast Cancer data processing
    """
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
        self.processed_data = {}
        self.feature_columns = {}
        self.target_columns = {}
        
    def load_and_clean_data(self) -> Dict[str, pd.DataFrame]:
        """Load and perform initial cleaning of all TSV files with memory optimization"""
        print("🔄 Loading and cleaning TCGA data...")
        
        data_files = {
            'clinical': 'clinical.tsv',
            'pathology_detail': 'pathology_detail.tsv',
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
        
        for name, filename in data_files.items():
            file_path = self.data_dir / filename
            if file_path.exists():
                print(f"📊 Processing {name} data...")
                try:
                    # Use chunking for large files to avoid memory issues
                    if name in ['clinical', 'follow_up', 'aliquot']:
                        # Read in chunks for large files
                        chunks = []
                        chunk_size = 1000
                        for chunk in pd.read_csv(file_path, sep='\t', chunksize=chunk_size):
                            chunks.append(chunk)
                        df = pd.concat(chunks, ignore_index=True)
                    else:
                        df = pd.read_csv(file_path, sep='\t')
                    
                    # Basic cleaning
                    df = self._clean_dataframe(df)
                    cleaned_data[name] = df
                    print(f"   ✅ Loaded {len(df)} rows, {len(df.columns)} columns")
                    
                except Exception as e:
                    print(f"   ❌ Error loading {name}: {str(e)}")
                    cleaned_data[name] = pd.DataFrame()
            else:
                print(f"   ⚠️ File {filename} not found")
                cleaned_data[name] = pd.DataFrame()
        
        return cleaned_data
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe with memory optimization"""
        # Convert object columns to category for memory efficiency
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:  # Only convert if cardinality is reasonable
                df[col] = df[col].astype('category')
        
        # Convert numeric columns to appropriate dtypes
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def extract_target_variables(self, data: Dict[str, pd.DataFrame]) -> Dict[str, List[str]]:
        """Extract target variables for each prediction task"""
        print("🎯 Extracting target variables...")
        
        targets = {
            'malignancy': [],
            'cancer_type': [],
            'metastasis': [],
            'tissue_change': [],
            'prognosis': [],
            'therapeutic_actions': [],
            'genetic_causes': []
        }
        
        # Extract malignancy indicators
        for df_name, df in data.items():
            if not df.empty:
                for col in df.columns:
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['malignant', 'benign', 'tumor', 'cancer']):
                        targets['malignancy'].append(f"{df_name}.{col}")
                    if any(keyword in col_lower for keyword in ['type', 'subtype', 'classification']):
                        targets['cancer_type'].append(f"{df_name}.{col}")
                    if any(keyword in col_lower for keyword in ['metastasis', 'metastatic', 'lymph_node']):
                        targets['metastasis'].append(f"{df_name}.{col}")
                    if any(keyword in col_lower for keyword in ['hyperplasia', 'dysplasia', 'carcinoma']):
                        targets['tissue_change'].append(f"{df_name}.{col}")
                    if any(keyword in col_lower for keyword in ['prognosis', 'survival', 'outcome']):
                        targets['prognosis'].append(f"{df_name}.{col}")
                    if any(keyword in col_lower for keyword in ['treatment', 'therapy', 'drug']):
                        targets['therapeutic_actions'].append(f"{df_name}.{col}")
                    if any(keyword in col_lower for keyword in ['mutation', 'gene', 'genetic']):
                        targets['genetic_causes'].append(f"{df_name}.{col}")
        
        # Print found columns
        for target_type, columns in targets.items():
            if columns:
                print(f"   Found {target_type} columns: {columns[:5]}...")  # Show first 5
        
        return targets
    
    def extract_features(self, data: Dict[str, pd.DataFrame]) -> Dict[str, List[str]]:
        """Extract feature columns for ML models"""
        print("🔍 Extracting features...")
        
        features = {
            'demographic': [],
            'clinical': [],
            'pathological': [],
            'genomic': [],
            'exposure': []
        }
        
        # Define feature categories
        demographic_keywords = ['age', 'gender', 'race', 'ethnicity', 'height', 'weight', 'bmi']
        clinical_keywords = ['diagnosis', 'stage', 'grade', 'tumor', 'treatment']
        pathological_keywords = ['pathology', 'histology', 'biopsy', 'surgery']
        genomic_keywords = ['gene', 'mutation', 'expression', 'sequence', 'chromosome']
        exposure_keywords = ['smoking', 'alcohol', 'radiation', 'chemical', 'environment']
        
        for df_name, df in data.items():
            if not df.empty:
                for col in df.columns:
                    col_lower = col.lower()
                    
                    if any(keyword in col_lower for keyword in demographic_keywords):
                        features['demographic'].append(f"{df_name}.{col}")
                    elif any(keyword in col_lower for keyword in clinical_keywords):
                        features['clinical'].append(f"{df_name}.{col}")
                    elif any(keyword in col_lower for keyword in pathological_keywords):
                        features['pathological'].append(f"{df_name}.{col}")
                    elif any(keyword in col_lower for keyword in genomic_keywords):
                        features['genomic'].append(f"{df_name}.{col}")
                    elif any(keyword in col_lower for keyword in exposure_keywords):
                        features['exposure'].append(f"{df_name}.{col}")
        
        # Print feature counts
        for feature_type, columns in features.items():
            if columns:
                print(f"   Extracted {len(columns)} {feature_type} features")
        
        return features
    
    def create_unified_dataset(self, data: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, Dict[str, List[str]]]:
        """Create unified dataset with memory optimization"""
        print("🔗 Creating unified dataset...")
        
        # Start with clinical data as base
        base_df = data.get('clinical', pd.DataFrame())
        if base_df.empty:
            print("❌ No clinical data found!")
            return pd.DataFrame(), {}
        
        # Get case identifier column
        case_col = None
        for col in base_df.columns:
            if 'case' in col.lower() or 'patient' in col.lower() or 'id' in col.lower():
                case_col = col
                break
        
        if case_col is None:
            case_col = base_df.columns[0]  # Use first column as key
        
        print(f"   Using '{case_col}' as case identifier")
        
        # Merge data step by step to avoid memory issues
        unified_df = base_df.copy()
        
        # Merge pathology data
        if 'pathology_detail' in data and not data['pathology_detail'].empty:
            path_df = data['pathology_detail']
            if case_col in path_df.columns:
                unified_df = unified_df.merge(
                    path_df, 
                    on=case_col, 
                    how='left', 
                    suffixes=('', '_pathology')
                )
                print(f"   Merged pathology data: {unified_df.shape}")
        
        # Merge sample data
        if 'sample' in data and not data['sample'].empty:
            sample_df = data['sample']
            if case_col in sample_df.columns:
                unified_df = unified_df.merge(
                    sample_df, 
                    on=case_col, 
                    how='left', 
                    suffixes=('', '_sample')
                )
                print(f"   Merged sample data: {unified_df.shape}")
        
        # Merge follow-up data (limit columns to avoid memory issues)
        if 'follow_up' in data and not data['follow_up'].empty:
            follow_df = data['follow_up']
            if case_col in follow_df.columns:
                # Select only important follow-up columns
                important_cols = [case_col] + [col for col in follow_df.columns 
                                             if any(keyword in col.lower() 
                                                   for keyword in ['survival', 'outcome', 'recurrence', 'metastasis'])]
                follow_subset = follow_df[important_cols]
                unified_df = unified_df.merge(
                    follow_subset, 
                    on=case_col, 
                    how='left', 
                    suffixes=('', '_follow')
                )
                print(f"   Merged follow-up data: {unified_df.shape}")
        
        # Merge exposure data
        if 'exposure' in data and not data['exposure'].empty:
            exp_df = data['exposure']
            if case_col in exp_df.columns:
                unified_df = unified_df.merge(
                    exp_df, 
                    on=case_col, 
                    how='left', 
                    suffixes=('', '_exposure')
                )
                print(f"   Merged exposure data: {unified_df.shape}")
        
        # Clean up memory
        del data
        import gc
        gc.collect()
        
        return unified_df
    
    def prepare_ml_data(self, unified_df: pd.DataFrame, targets: Dict[str, List[str]]) -> Tuple[pd.DataFrame, Dict[str, pd.Series]]:
        """Prepare data for machine learning"""
        print("🤖 Preparing ML data...")
        
        # Handle missing values
        unified_df = unified_df.fillna(unified_df.mode().iloc[0] if not unified_df.mode().empty else 0)
        
        # Convert categorical variables
        categorical_cols = unified_df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            unified_df[col] = pd.Categorical(unified_df[col]).codes
        
        # Create target variables
        target_variables = {}
        for target_type, columns in targets.items():
            if columns:
                # Find actual columns in the dataset
                available_cols = [col for col in columns if col in unified_df.columns]
                if available_cols:
                    # Use the first available column as target
                    target_variables[target_type] = unified_df[available_cols[0]]
                    print(f"   Created target: {target_type} using {available_cols[0]}")
        
        return unified_df, target_variables
    
    def run_pipeline(self) -> Tuple[pd.DataFrame, Dict[str, pd.Series]]:
        """Run the complete data pipeline"""
        print("🚀 Starting TCGA Breast Cancer Data Pipeline")
        print("=" * 60)
        
        # Load and clean data
        data = self.load_and_clean_data()
        
        # Extract targets and features
        targets = self.extract_target_variables(data)
        features = self.extract_features(data)
        
        # Create unified dataset
        unified_df = self.create_unified_dataset(data)
        
        if unified_df.empty:
            print("❌ Failed to create unified dataset!")
            return pd.DataFrame(), {}
        
        # Prepare ML data
        ml_data, target_variables = self.prepare_ml_data(unified_df, targets)
        
        print(f"\n✅ Pipeline completed successfully!")
        print(f"📊 Final dataset shape: {ml_data.shape}")
        print(f"🎯 Target variables: {list(target_variables.keys())}")
        
        # Save processed data
        ml_data.to_csv('processed_ml_data.csv', index=False)
        print("💾 Saved processed data to 'processed_ml_data.csv'")
        
        return ml_data, target_variables

if __name__ == "__main__":
    pipeline = TCGA_BreastCancerPipeline()
    ml_data, targets = pipeline.run_pipeline() 