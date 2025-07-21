import re
import glob
import os

input_dir = 'frontend/public/'
pattern = os.path.join(input_dir, 'batch_template_*.csv')
files = glob.glob(pattern)

for input_path in files:
    output_path = input_path.replace('.csv', '_clean.csv')
    with open(input_path, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
    cleaned_lines = []
    for line in lines:
        cleaned = re.sub(r',\s+', ',', line.rstrip())
        cleaned_lines.append(cleaned)
    with open(output_path, 'w', encoding='utf-8', newline='') as fout:
        for line in cleaned_lines:
            fout.write(line + '\n')
    print(f'Cleaned CSV written to {output_path}') 