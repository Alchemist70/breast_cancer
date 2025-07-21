import pandas as pd
import numpy as np
import os
from pathlib import Path
import json

def analyze_tsv_file(file_path, max_rows=5):
    """Analyze a TSV file and return basic information"""
    try:
        # Read just the header and first few rows
        df = pd.read_csv(file_path, sep='\t', nrows=max_rows)
        
        # Get file size
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        
        analysis = {
            'file_name': os.path.basename(file_path),
            'file_size_mb': round(file_size, 2),
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'sample_data': df.head(2).to_dict('records'),
            'dtypes': df.dtypes.to_dict()
        }
        
        return analysis
    except Exception as e:
        return {
            'file_name': os.path.basename(file_path),
            'error': str(e)
        }

def main():
    """Analyze all TSV files in the current directory"""
    print("🔍 Analyzing TCGA Breast Cancer Data Files...")
    print("=" * 60)
    
    # Get all TSV files
    tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]
    
    all_analyses = {}
    
    for file_path in tsv_files:
        print(f"\n📊 Analyzing: {file_path}")
        analysis = analyze_tsv_file(file_path)
        all_analyses[file_path] = analysis
        
        if 'error' not in analysis:
            print(f"   Size: {analysis['file_size_mb']} MB")
            print(f"   Shape: {analysis['shape']}")
            print(f"   Columns: {len(analysis['columns'])}")
            print(f"   Sample columns: {analysis['columns'][:5]}...")
        else:
            print(f"   Error: {analysis['error']}")
    
    # Save analysis to JSON for reference
    with open('data_analysis.json', 'w') as f:
        json.dump(all_analyses, f, indent=2, default=str)
    
    print(f"\n✅ Analysis complete! Results saved to 'data_analysis.json'")
    
    # Identify key files for different aspects
    print("\n🎯 Key Data Files Identified:")
    print("-" * 40)
    
    for file_path, analysis in all_analyses.items():
        if 'error' not in analysis:
            if 'clinical' in file_path.lower():
                print(f"📋 Clinical Data: {file_path} ({analysis['file_size_mb']} MB)")
            elif 'pathology' in file_path.lower():
                print(f"🔬 Pathology Data: {file_path} ({analysis['file_size_mb']} MB)")
            elif 'sample' in file_path.lower():
                print(f"🧬 Sample Data: {file_path} ({analysis['file_size_mb']} MB)")
            elif 'follow_up' in file_path.lower():
                print(f"📈 Follow-up Data: {file_path} ({analysis['file_size_mb']} MB)")
            elif 'exposure' in file_path.lower():
                print(f"🌍 Exposure Data: {file_path} ({analysis['file_size_mb']} MB)")
            elif 'family_history' in file_path.lower():
                print(f"👨‍👩‍👧‍👦 Family History: {file_path} ({analysis['file_size_mb']} MB)")

if __name__ == "__main__":
    main() 