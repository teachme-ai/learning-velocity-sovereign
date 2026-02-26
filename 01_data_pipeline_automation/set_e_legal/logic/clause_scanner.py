import os
import json
import re

def scan_contract(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    scanned_data = []
    risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, 'r') as infile:
        content = infile.read()
        
    # Split by empty lines to get discrete clauses
    clauses = [c.strip() for c in content.split('\n\n') if c.strip()]
    
    for clause in clauses:
        risk_level = "LOW"
        risk_tags = []
        
        # Keyword mappings
        if re.search(r'Uncapped Liability', clause, re.IGNORECASE):
            risk_level = "HIGH"
            risk_tags.append("UNLIMITED_LIABILITY")
            
        if re.search(r'30-day termination without cause', clause, re.IGNORECASE):
            risk_level = "MEDIUM"
            risk_tags.append("AT_WILL_TERMINATION")
            
        if re.search(r'15 years', clause, re.IGNORECASE):
            risk_level = "HIGH"
            risk_tags.append("EXCESSIVE_NON_COMPETE")
            
        risk_counts[risk_level] += 1
        scanned_data.append({
            "extracted_clause": clause,
            "risk_assessment": risk_level,
            "tags": risk_tags
        })

    with open(output_file, 'w') as outfile:
        json.dump({
            "summary": risk_counts,
            "clauses": scanned_data
        }, outfile, indent=2)

    print(f"Legal Contract Scanning complete.")
    print(f"Total clauses evaluated: {len(clauses)}")
    print(f"High risks found: {risk_counts['HIGH']}")
    print(f"Extraction mapped to {output_file}")


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    input_text = os.path.join(base_dir, '../data/contract_snippets.txt')
    
    # We write to /tmp to bypass Mac SIP / Sandbox environments safely.
    output_dir = '/tmp/legal_output'
    os.makedirs(output_dir, exist_ok=True)
    output_json = os.path.join(output_dir, 'scanned_clauses.json')
    
    scan_contract(input_text, output_json)
