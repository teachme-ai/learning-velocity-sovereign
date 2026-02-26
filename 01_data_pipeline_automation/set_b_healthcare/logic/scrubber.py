import csv
import re
from datetime import datetime
import os

def determine_pii(patient_id):
    # Weak PII check for demo
    # If it contains space and purely alphabetical, it's likely a Name
    parts = patient_id.split(' ')
    if len(parts) >= 2 and all(p.isalpha() for p in parts):
        return True
    return False

def scrub_data(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    cleaned_data = []
    issues_found = 0
    anonymized_count = 0

    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        # We might add a 'flag_reason' column if it's dirty
        if 'flag_reason' not in fieldnames:
            fieldnames.append('flag_reason')

        for row_num, row in enumerate(reader, start=2): # Start at 2 to account for header
            flags = []
            
            # 1. Anonymize PII
            patient_id = row['patient_id']
            if determine_pii(patient_id):
                # Replace with anonymous ID
                anonymized_id = f"ANON-{abs(hash(patient_id)) % 100000}"
                row['patient_id'] = anonymized_id
                anonymized_count += 1
                flags.append("PII_ANONYMIZED")

            # 2. Admit Date check (no future dates)
            try:
                admit_date = datetime.strptime(row['admission_date'], '%Y-%m-%d')
                if admit_date > datetime.now():
                    flags.append("FUTURE_ADMISSION_DATE")
            except ValueError:
                flags.append("INVALID_DATE_FORMAT")

            # 3. Diagnosis Code format check (1 Letter + 2 Digits)
            # basic regex: ^[A-Z][0-9]{2}(\.[0-9]+)?$
            diag_code = row['diagnosis_code']
            if not re.match(r'^[A-Z][0-9]{2}$', diag_code):
                flags.append("MALFORMED_ICD_CODE")

            # 4. Treatment Cost Validity
            try:
                cost = float(row['treatment_cost'])
                if cost <= 0:
                    flags.append("INVALID_COST")
            except ValueError:
                flags.append("NON_NUMERIC_COST")

            row['flag_reason'] = " | ".join(flags)
            if flags and flags != ["PII_ANONYMIZED"]:
                # If there are actual errors (not just anonymization)
                issues_found += 1
                
            cleaned_data.append(row)

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"Scrubbing complete.")
    print(f"Total rows processed: {len(cleaned_data)}")
    print(f"PII Anonymized: {anonymized_count} rows")
    print(f"Rows with Validation Flags: {issues_found}")
    print(f"Cleaned output saved to {output_file}")


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    input_csv = os.path.join(base_dir, '../data/patient_billing.csv')
    output_dir = '/tmp/healthcare_output'
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, 'scrubbed_billing.csv')
    scrub_data(input_csv, output_csv)
