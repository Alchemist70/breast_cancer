import pandas as pd
import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class GenomicFeatureExtractor:
    """
    Efficiently extract genomic features from large TCGA files
    """
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = Path(data_dir)
        
    def get_file_headers(self, filename: str) -> List[str]:
        """Get column headers from a TSV file efficiently"""
        try:
            # Read only the header row
            df_header = pd.read_csv(filename, sep='\t', nrows=0)
            return df_header.columns.tolist()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return []
    
    def extract_genomic_features(self):
        """Extract genomic features from all relevant files"""
        print("🧬 Extracting genomic features...")
        
        genomic_features = {}
        
        # Analyze aliquot.tsv
        print("📊 Analyzing aliquot.tsv...")
        aliquot_cols = self.get_file_headers('aliquot.tsv')
        if aliquot_cols:
            genomic_features['aliquot'] = {
                'columns': aliquot_cols,
                'genomic_cols': [col for col in aliquot_cols if any(keyword in col.lower() 
                                   for keyword in ['concentration', 'quantity', 'volume', 'amount', 'analyte'])]
            }
            print(f"   Found {len(genomic_features['aliquot']['genomic_cols'])} genomic columns")
        
        # Analyze analyte.tsv
        print("📊 Analyzing analyte.tsv...")
        analyte_cols = self.get_file_headers('analyte.tsv')
        if analyte_cols:
            genomic_features['analyte'] = {
                'columns': analyte_cols,
                'genomic_cols': [col for col in analyte_cols if any(keyword in col.lower() 
                                   for keyword in ['concentration', 'integrity', 'quality', 'ratio'])]
            }
            print(f"   Found {len(genomic_features['analyte']['genomic_cols'])} genomic columns")
        
        # Analyze follow_up.tsv for molecular data
        print("📊 Analyzing follow_up.tsv for molecular data...")
        follow_up_cols = self.get_file_headers('follow_up.tsv')
        if follow_up_cols:
            molecular_cols = [col for col in follow_up_cols if 'molecular_tests' in col]
            genomic_features['molecular'] = {
                'columns': molecular_cols,
                'genomic_cols': molecular_cols
            }
            print(f"   Found {len(molecular_cols)} molecular test columns")
        
        return genomic_features
    
    def create_genomic_mapping(self, genomic_features: Dict) -> Dict:
        """Create a mapping of genomic features to prediction targets"""
        print("🗺️ Creating genomic feature mapping...")
        
        mapping = {
            'genetic_causes': [],
            'genomic_quality': [],
            'molecular_markers': [],
            'sequencing_data': []
        }
        
        # Map genetic causes
        if 'molecular' in genomic_features:
            genetic_cols = [col for col in genomic_features['molecular']['genomic_cols'] 
                          if any(keyword in col.lower() for keyword in ['gene', 'mutation', 'chromosome'])]
            mapping['genetic_causes'] = genetic_cols
        
        # Map genomic quality
        if 'analyte' in genomic_features:
            quality_cols = [col for col in genomic_features['analyte']['genomic_cols'] 
                          if any(keyword in col.lower() for keyword in ['integrity', 'quality', 'concentration'])]
            mapping['genomic_quality'] = quality_cols
        
        # Map molecular markers
        if 'molecular' in genomic_features:
            marker_cols = [col for col in genomic_features['molecular']['genomic_cols'] 
                         if any(keyword in col.lower() for keyword in ['test_result', 'test_value', 'antigen'])]
            mapping['molecular_markers'] = marker_cols
        
        # Map sequencing data
        if 'aliquot' in genomic_features:
            seq_cols = [col for col in genomic_features['aliquot']['genomic_cols'] 
                       if any(keyword in col.lower() for keyword in ['sequencing', 'wgs', 'targeted'])]
            mapping['sequencing_data'] = seq_cols
        
        return mapping
    
    def update_main_dataset(self, genomic_features: Dict, genomic_mapping: Dict):
        """Update the main ML dataset with genomic features"""
        print("🔄 Updating main dataset with genomic features...")
        
        # Load the existing ML dataset
        try:
            ml_data = pd.read_csv('breast_cancer_ml_data.csv')
            print(f"   Loaded existing dataset: {ml_data.shape}")
        except:
            print("   No existing ML dataset found")
            return
        
        # Load genomic data in chunks to avoid memory issues
        genomic_data = {}
        
        # Load aliquot data if available
        if 'aliquot' in genomic_features:
            try:
                # Read aliquot data in chunks
                aliquot_chunks = []
                chunk_size = 1000
                for chunk in pd.read_csv('aliquot.tsv', sep='\t', chunksize=chunk_size):
                    # Select only genomic columns and linking keys
                    genomic_cols = genomic_features['aliquot']['genomic_cols']
                    linking_cols = ['cases.case_id', 'samples.sample_id']
                    available_cols = [col for col in genomic_cols + linking_cols if col in chunk.columns]
                    if available_cols:
                        aliquot_chunks.append(chunk[available_cols])
                
                if aliquot_chunks:
                    genomic_data['aliquot'] = pd.concat(aliquot_chunks, ignore_index=True)
                    print(f"   Loaded aliquot data: {genomic_data['aliquot'].shape}")
            except Exception as e:
                print(f"   Error loading aliquot data: {e}")
        
        # Load analyte data if available
        if 'analyte' in genomic_features:
            try:
                # Read analyte data in chunks
                analyte_chunks = []
                chunk_size = 1000
                for chunk in pd.read_csv('analyte.tsv', sep='\t', chunksize=chunk_size):
                    # Select only genomic columns and linking keys
                    genomic_cols = genomic_features['analyte']['genomic_cols']
                    linking_cols = ['cases.case_id', 'samples.sample_id']
                    available_cols = [col for col in genomic_cols + linking_cols if col in chunk.columns]
                    if available_cols:
                        analyte_chunks.append(chunk[available_cols])
                
                if analyte_chunks:
                    genomic_data['analyte'] = pd.concat(analyte_chunks, ignore_index=True)
                    print(f"   Loaded analyte data: {genomic_data['analyte'].shape}")
            except Exception as e:
                print(f"   Error loading analyte data: {e}")
        
        # Merge genomic data with main dataset
        updated_ml_data = ml_data.copy()
        
        for data_type, data_df in genomic_data.items():
            if not data_df.empty:
                # Find common linking columns
                common_cols = set(ml_data.columns) & set(data_df.columns)
                if common_cols:
                    merge_col = list(common_cols)[0]
                    
                    # Convert data types to string to avoid merge issues
                    ml_data_copy = ml_data.copy()
                    data_df_copy = data_df.copy()
                    
                    # Convert merge column to string in both dataframes
                    if merge_col in ml_data_copy.columns:
                        ml_data_copy[merge_col] = ml_data_copy[merge_col].astype(str)
                    if merge_col in data_df_copy.columns:
                        data_df_copy[merge_col] = data_df_copy[merge_col].astype(str)
                    
                    updated_ml_data = ml_data_copy.merge(
                        data_df_copy, 
                        on=merge_col, 
                        how='left', 
                        suffixes=('', f'_{data_type}')
                    )
                    print(f"   Merged {data_type} data using '{merge_col}'")
        
        # Save updated dataset
        updated_ml_data.to_csv('breast_cancer_ml_data_with_genomics.csv', index=False)
        print(f"   ✅ Saved updated dataset: {updated_ml_data.shape}")
        
        # Save genomic mapping
        with open('genomic_feature_mapping.json', 'w') as f:
            json.dump(genomic_mapping, f, indent=2)
        print("   💾 Saved genomic feature mapping")
        
        return updated_ml_data
    
    def run_extraction(self):
        """Run the complete genomic feature extraction"""
        print("🚀 Starting Genomic Feature Extraction")
        print("=" * 50)
        
        # Extract genomic features
        genomic_features = self.extract_genomic_features()
        
        # Create mapping
        genomic_mapping = self.create_genomic_mapping(genomic_features)
        
        # Update main dataset
        updated_data = self.update_main_dataset(genomic_features, genomic_mapping)
        
        # Print summary
        print(f"\n✅ Genomic feature extraction completed!")
        print(f"🧬 Genomic features found:")
        for category, features in genomic_mapping.items():
            if features:
                print(f"   {category}: {len(features)} features")
        
        return updated_data

if __name__ == "__main__":
    extractor = GenomicFeatureExtractor()
    updated_data = extractor.run_extraction() 