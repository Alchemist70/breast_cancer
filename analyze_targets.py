import pandas as pd
import numpy as np

def analyze_potential_targets():
    """Analyze all data files to find potential new targets"""
    print("🔍 Analyzing potential new targets...")
    
    # Check clinical data
    print("\n📊 Clinical Data Analysis:")
    clinical_df = pd.read_csv('clinical.tsv', sep='\t')
    
    potential_targets = []
    
    for col in clinical_df.columns:
        if col.startswith('diagnoses.') or col.startswith('demographic.') or col.startswith('treatments.'):
            unique_vals = clinical_df[col].value_counts()
            valid_vals = unique_vals[unique_vals.index != "'--"]
            valid_vals = valid_vals[valid_vals.index != 'Not Reported']
            
            if len(valid_vals) >= 2 and valid_vals.iloc[0] >= 50:
                potential_targets.append({
                    'column': col,
                    'unique_values': len(valid_vals),
                    'top_values': valid_vals.head(3).to_dict(),
                    'total_valid': valid_vals.sum()
                })
    
    # Sort by total valid samples
    potential_targets.sort(key=lambda x: x['total_valid'], reverse=True)
    
    print(f"\n🎯 Found {len(potential_targets)} potential targets:")
    for i, target in enumerate(potential_targets[:15], 1):
        print(f"\n{i}. {target['column']}")
        print(f"   Valid samples: {target['total_valid']}")
        print(f"   Unique values: {target['unique_values']}")
        print(f"   Top values: {target['top_values']}")
    
    # Check follow-up data
    print("\n📊 Follow-up Data Analysis:")
    try:
        followup_df = pd.read_csv('follow_up.tsv', sep='\t')
        
        followup_targets = []
        for col in followup_df.columns:
            if col.startswith('follow_ups.'):
                unique_vals = followup_df[col].value_counts()
                valid_vals = unique_vals[unique_vals.index != "'--"]
                valid_vals = valid_vals[valid_vals.index != 'Not Reported']
                
                if len(valid_vals) >= 2 and valid_vals.iloc[0] >= 20:
                    followup_targets.append({
                        'column': col,
                        'unique_values': len(valid_vals),
                        'top_values': valid_vals.head(3).to_dict(),
                        'total_valid': valid_vals.sum()
                    })
        
        followup_targets.sort(key=lambda x: x['total_valid'], reverse=True)
        
        print(f"\n🎯 Found {len(followup_targets)} potential follow-up targets:")
        for i, target in enumerate(followup_targets[:10], 1):
            print(f"\n{i}. {target['column']}")
            print(f"   Valid samples: {target['total_valid']}")
            print(f"   Unique values: {target['unique_values']}")
            print(f"   Top values: {target['top_values']}")
            
    except Exception as e:
        print(f"Error reading follow-up data: {e}")
    
    return potential_targets + followup_targets

if __name__ == "__main__":
    analyze_potential_targets() 