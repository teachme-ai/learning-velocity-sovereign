import os
import sys
import json
import ollama
import csv

def generate_dirty_data(slug, industry):
    """Generate 50 rows of dirty CSV data for a specific industry using Ollama."""
    print(f"🧬 Generating 50 rows of synthetic data for {industry}...")
    
    prompt = f"""
    Retail industry expense data CSV. 50 rows.
    Columns: transaction_id,date,employee_id,department,category,description,amount_usd
    Items: Returns, Footwear, Inventory, Refunds, SKU mismatches.
    
    Format:
    transaction_id,date,employee_id,department,category,description,amount_usd
    TXN-001,2024-01-01,EMP-10,Sales,Product,Description,10.00
    
    START CSV NOW.
    """
    
    try:
        response = ollama.chat(model='llama3.2:1b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        csv_content = response['message']['content'].strip()
        
        # Ensure we only have the CSV part if the LLM added chatter
        if "transaction_id" in csv_content:
            csv_content = csv_content[csv_content.find("transaction_id"):]
            
        # Write to the template directory so it's ready for the compiler
        # Since the sessions are now universal, we put it in the data folder of Session 01 template
        target_dir = os.path.join(os.path.dirname(__file__), "../../../_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data")
        os.makedirs(target_dir, exist_ok=True)
        
        target_file = os.path.join(target_dir, "dirty_data.csv")
        # Note: We also need it as 'corporate_expenses.csv' for the Finance logic we are templating
        # Let's write both to be safe or just use a generic name in the template logic later.
        
        with open(target_file, 'w') as f:
            f.write(csv_content)
            
        # For compatibility with existing Finance-based logic
        with open(os.path.join(target_dir, "corporate_expenses.csv"), 'w') as f:
            f.write(csv_content)
            
        print(f"✅ Data written to {target_file}")
    except Exception as e:
        print(f"❌ Failed to generate synthetic data: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 data_synth.py <slug> <industry>")
        sys.exit(1)
    generate_dirty_data(sys.argv[1], sys.argv[2])
