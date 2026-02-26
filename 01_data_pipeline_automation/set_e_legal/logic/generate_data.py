import os
import random

def generate_legal_data(num_snippets=25):
    snippets = []
    
    benign_clauses = [
        "The effective date of this agreement is defined globally in Section 2.1.",
        "Both parties agree to standard arbitration procedures in the venue of New York.",
        "Notice must be provided in writing and delivered via certified mail."
    ]
    
    risky_clauses = [
        "[RISK] Party A assumes Uncapped Liability for all indirect, punitive, or consequential damages resulting from this agreement.",
        "[RISK] The vendor retains the right to execute a 30-day termination without cause at any juncture.",
        "[RISK] Non-compete restrictions shall persist globally for a term of no less than 15 years."
    ]
    
    for _ in range(num_snippets):
        is_risky = random.random() < 0.25 # 25% chance of risky clause
        
        if is_risky:
            clause = random.choice(risky_clauses)
        else:
            clause = random.choice(benign_clauses)
            
        snippets.append(clause)
        
    return snippets

if __name__ == '__main__':
    data = generate_legal_data(30)
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    output_dir = os.path.join(base_dir, '../data')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'contract_snippets.txt')
    with open(output_file, 'w') as f:
        for line in data:
            f.write(line + "\n\n")
            
    print(f"Successfully generated 30 raw contract clauses to {output_file}")
