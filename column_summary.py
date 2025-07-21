import pandas as pd

def summarize_columns(filename, name, n_sample=5):
    print(f'--- {name} ---')
    df = pd.read_csv(filename, sep='\t', low_memory=False)
    print(f'Shape: {df.shape}')
    for col in df.columns:
        vals = df[col].dropna().unique()
        print(f'{col}: {len(vals)} unique, sample: {vals[:n_sample]}')

import sys
sys.stdout = open('column_summary.txt', 'w', encoding='utf-8')

summarize_columns('clinical.tsv', 'Clinical')
summarize_columns('pathology_detail.tsv', 'Pathology')
summarize_columns('follow_up.tsv', 'Follow-up') 