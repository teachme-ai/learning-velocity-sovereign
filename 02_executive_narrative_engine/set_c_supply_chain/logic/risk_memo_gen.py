import csv
import json
import urllib.request
import os

def generate_risk_memo(input_csv, output_md):
    if not os.path.exists(input_csv):
        print(f"Error: Could not find scrubbed inventory data at {input_csv}")
        return

    total_records = 0
    anomalies_caught = 0
    malformed_skus = set()
    pricing_errors = 0

    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            flags = row.get('flag_reason', '')
            
            if flags:
                anomalies_caught += 1
            if 'MALFORMED_SKU' in flags:
                malformed_skus.add(row['item_sku'])
            if 'INVALID_PRICE' in flags or 'HIGH_VALUE_REVIEW_REQUIRED' in flags:
                pricing_errors += 1

    prompt = f"""You are a senior supply chain AI auditor for a distributed warehouse network.
Analyze this data summary and output a comprehensive 'Logistics Risk Memo' in Markdown format.

Data Insights:
- Total inventory logs processed: {total_records}
- Number of anomalies/stock issues caught: {anomalies_caught}
- Pricing integrity errors found: {pricing_errors}
- Malformed SKUs flagged: {', '.join(malformed_skus) if malformed_skus else 'None found'}

Requirements:
1. Provide a professional, executive summary of the inventory quality.
2. Under exactly one professional recommendation header, advise on how to proactively prevent these SKU formatting errors and pricing anomalies from contaminating the centralized inventory catalog.
3. Keep the entire response under 300 words. Focus strictly on actionable operational advice. Do not ask me a question or begin with a greeting.
"""

    print("Sending supply chain summary to Local Ollama model (llama3.2:1b)...")
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            report_text = result.get('response', '')
            
            os.makedirs(os.path.dirname(output_md), exist_ok=True)
            with open(output_md, 'w') as out:
                out.write(report_text)
                
            print(f"Logistics Risk Memo successfully generated and saved to: {output_md}")
            
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Ensure 'ollama run llama3.2:1b' is active.")


if __name__ == '__main__':
    input_file = '/tmp/supply_chain_output/scrubbed_inventory.csv'
    output_file = '/tmp/supply_chain_output/risk_memo.md'
    
    generate_risk_memo(input_file, output_file)
