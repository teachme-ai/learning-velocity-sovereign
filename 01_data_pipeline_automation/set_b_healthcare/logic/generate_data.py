import csv
import random
from datetime import datetime, timedelta

def generate_data(num_rows=50):
    data = []
    
    # Standard ICD-10 codes (Alpha + 2 digits)
    valid_icd_codes = ['J01', 'E11', 'I10', 'A09', 'K21', 'M54']
    malformed_icd_codes = ['10J', 'E-11', 'A09X', 'M54.Z']

    # Sample Names for PII
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'James', 'Jessica', 'Robert', 'Ashley']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    insurance_providers = ['BlueCross', 'Aetna', 'UnitedHealth', 'Cigna', 'Humana', 'Medicare']
    
    start_date = datetime.now() - timedelta(days=365)

    for i in range(num_rows):
        is_dirty = random.random() < 0.2  # 20% chance of dirty data
        has_pii = random.random() < 0.5   # 50% chance of including PII (Name instead of ID)
        
        # 1. Patient ID / PII
        if has_pii:
            patient_id = f"{random.choice(first_names)} {random.choice(last_names)}"
        else:
            patient_id = f"P-{random.randint(10000, 99999)}"
        
        # 2. Admission Date (Some dirty data: future dates)
        days_offset = random.randint(0, 365)
        admit_date = start_date + timedelta(days=days_offset)
        if is_dirty and random.random() < 0.3:
            # Future date
            admit_date = datetime.now() + timedelta(days=random.randint(1, 30))
            
        admission_date_str = admit_date.strftime('%Y-%m-%d')
        
        # 3. Diagnosis Code
        if is_dirty and random.random() < 0.4:
            diagnosis_code = random.choice(malformed_icd_codes)
        else:
            diagnosis_code = random.choice(valid_icd_codes)
            
        # 4. Treatment Cost
        if is_dirty and random.random() < 0.5:
            # Negative or zero cost
            treatment_cost = round(random.uniform(-1000, 0), 2)
        else:
            treatment_cost = round(random.uniform(50, 5000), 2)
            
        # 5. Insurance Provider
        insurance_provider = random.choice(insurance_providers)
        
        data.append({
            'patient_id': patient_id,
            'admission_date': admission_date_str,
            'diagnosis_code': diagnosis_code,
            'treatment_cost': treatment_cost,
            'insurance_provider': insurance_provider
        })
        
    return data

if __name__ == '__main__':
    header = ['patient_id', 'admission_date', 'diagnosis_code', 'treatment_cost', 'insurance_provider']
    data = generate_data(50)
    
    output_file = '01_data_pipeline_automation/set_b_healthcare/data/patient_billing.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"Successfully generated 50 rows of patient billing data to {output_file}")
