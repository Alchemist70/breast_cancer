import csv

header = [
    "demographic.age_at_index",
    "diagnoses.tumor_grade",
    "diagnoses.ajcc_pathologic_stage",
    "diagnoses.tumor_size",
    "diagnoses.lymph_nodes_examined",
    "demographic.gender",
    "demographic.race",
    "demographic.ethnicity",
    "diagnoses.primary_diagnosis",
    "diagnoses.prior_malignancy"
]

def main():
    # Example data row (replace or extend as needed)
    data = [
        [65, 2, "Stage IIA", 25.5, 3, "female", "white", "not hispanic or latino", "Infiltrating duct carcinoma", "yes"],
        # Add more rows here or modify as needed
    ]

    with open("malignancy_batch_upload.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print("malignancy_batch_upload.csv has been created with the correct header.")

if __name__ == "__main__":
    main() 