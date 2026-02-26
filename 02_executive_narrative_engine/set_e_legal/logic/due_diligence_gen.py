import json
import urllib.request
import os

def generate_due_diligence(input_json, output_md):
    if not os.path.exists(input_json):
        print(f"Error: Could not find scanned clauses at {input_json}")
        return

    high_risks = 0
    med_risks = 0
    severe_clauses = []

    with open(input_json, 'r') as f:
        data = json.load(f)
        
        counts = data.get('summary', {})
        high_risks = counts.get('HIGH', 0)
        med_risks = counts.get('MEDIUM', 0)
        
        for clause in data.get('clauses', []):
            if clause['risk_assessment'] == 'HIGH':
                severe_clauses.append(clause['extracted_clause'])

    prompt = f"""You are a Senior Legal Counsel conducting M&A due diligence.
Analyze this structured risk map and output a strict 'Contract Due Diligence Brief' in Markdown format for the executive team.

Data Insights:
- Critical (HIGH) Liability Clauses Found: {high_risks}
- Medium Risk Clauses Found: {med_risks}
- Example Severe Clause Text: "{severe_clauses[0] if severe_clauses else 'None'}"

Requirements:
1. Synthesize the severity of the liabilities discovered into a professional summary.
2. Under exactly one professional recommendation header, outline the immediate remediation strategy for the Legal team.
3. Keep the entire response under 300 words. Be objective and robotic. Do not ask me a question or begin with a greeting.
"""

    print("Sending Legal Due Diligence summary to Local Ollama model (llama3.2:1b)...")
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
                
            print(f"Contract Due Diligence successfully generated and saved to: {output_md}")
            
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Ensure 'ollama run llama3.2:1b' is active.")


if __name__ == '__main__':
    input_file = '/tmp/legal_output/scanned_clauses.json'
    output_file = '/tmp/legal_output/due_diligence_brief.md'
    
    generate_due_diligence(input_file, output_file)
