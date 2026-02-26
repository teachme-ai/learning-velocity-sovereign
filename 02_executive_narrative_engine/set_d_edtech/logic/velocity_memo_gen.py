import csv
import json
import urllib.request
import os

def generate_velocity_memo(input_csv, output_md):
    if not os.path.exists(input_csv):
        print(f"Error: Could not find cleaned student logs at {input_csv}")
        return

    total_records = 0
    anomalies_caught = 0
    modules_flagged = set()

    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            flags = row.get('anomaly_flag', '')
            
            if flags:
                anomalies_caught += 1
                modules_flagged.add(row['Course_Module'])

    prompt = f"""You are a senior EdTech Data Scientist analyzing student progression.
Analyze this data summary and output a comprehensive 'Learning Velocity Memo' in Markdown format for the Faculty Board.

Data Insights:
- Total student logs processed: {total_records}
- Number of outlier/impossible records caught (e.g. negative time, >100 scores): {anomalies_caught}
- Course modules associated with dirty data: {', '.join(modules_flagged) if modules_flagged else 'None found'}

Requirements:
1. Provide a professional executive summary of the cohort's data integrity.
2. Under exactly one professional recommendation header, advise the curriculum designers on how to build safeguards into the learning management system (LMS) to prevent impossibility tracking.
3. Keep the entire response under 300 words. Focus strictly on actionable advice. Do not ask me a question or begin with a greeting.
"""

    print("Sending EdTech summary to Local Ollama model (llama3.2:1b)...")
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
                
            print(f"Learning Velocity Memo successfully generated and saved to: {output_md}")
            
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Ensure 'ollama run llama3.2:1b' is active.")


if __name__ == '__main__':
    input_file = '/tmp/edtech_output/cleaned_logs.csv'
    output_file = '/tmp/edtech_output/velocity_memo.md'
    
    generate_velocity_memo(input_file, output_file)
