import csv
import json
import urllib.request
import os

def generate_compliance_report(input_csv, output_md):
    if not os.path.exists(input_csv):
        print(f"Error: Could not find scrubbed input data at {input_csv}")
        return

    total_records = 0
    pii_violations = 0
    malformed_icd_codes = set()

    # Parse the data to obtain metrics
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            flags = row.get('flag_reason', '')
            if 'PII_ANONYMIZED' in flags:
                pii_violations += 1
            if 'MALFORMED_ICD_CODE' in flags:
                malformed_icd_codes.add(row['diagnosis_code'])

    # Build the prompt
    prompt = f"""You are a senior healthcare compliance AI auditor for a major hospital network.
Analyze this data summary and output a comprehensive 'Clinical Compliance Report' in Markdown format.

Data Insights:
- Total records processed: {total_records}
- PII violations caught & anonymized automatically: {pii_violations}
- Malformed ICD-10 codes flagged: {', '.join(malformed_icd_codes) if malformed_icd_codes else 'None found'}

Requirements:
1. Provide a professional, executive summary of the data quality.
2. Under exactly one professional recommendation header, advise the Hospital Administrator on how to proactively prevent these PII exposure and ICD-10 formatting errors at the data entry level before they reach the pipeline.
3. Keep the entire response under 300 words. Focus strictly on actionable advice. Do not ask me a question or begin with a greeting.
"""

    # Hit local Ollama
    print("Sending data proxy to Local Ollama model (llama3.2:1b)...")
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
            
            # Save the file
            os.makedirs(os.path.dirname(output_md), exist_ok=True)
            with open(output_md, 'w') as out:
                out.write(report_text)
                
            print(f"Compliance Report successfully generated and saved to: {output_md}")
            
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Ensure 'ollama run llama3.2:1b' is active.")

if __name__ == '__main__':
    # Due to Mac Sandbox restrictions seen in Session 01, we utilize /tmp for reliable read/writes if standard folder is blocked
    input_file = '/tmp/healthcare_output/scrubbed_billing.csv'
    output_file = '/tmp/healthcare_output/compliance_report.md'
    
    # If standard local path exists or tmp fails, we could fallback, but we know tmp route works.
    generate_compliance_report(input_file, output_file)
