import csv
import os

def clean_edtech_logs(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    cleaned_data = []
    issues_found = 0

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        if 'anomaly_flag' not in fieldnames:
            fieldnames.append('anomaly_flag')

        for row in reader:
            flags = []
            
            try:
                time_spent = int(row['Time_Spent'])
                if time_spent < 0:
                    flags.append("NEGATIVE_TIME")
            except ValueError:
                flags.append("INVALID_TIME_FORMAT")
                
            try:
                score = int(row['Score'])
                if score > 100:
                    flags.append("SCORE_OUT_OF_BOUNDS")
                elif score < 0:
                    flags.append("NEGATIVE_SCORE")
            except ValueError:
                flags.append("INVALID_SCORE_FORMAT")

            row['anomaly_flag'] = " | ".join(flags)
            if flags:
                issues_found += 1
                
            cleaned_data.append(row)

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"EdTech Velocity Cleansing complete.")
    print(f"Total rows processed: {len(cleaned_data)}")
    print(f"Rows with Anomalies Flagged: {issues_found}")
    print(f"Cleaned output saved to {output_file}")


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    input_csv = os.path.join(base_dir, '../data/student_logs.csv')
    
    # We write to /tmp to bypass Mac SIP / Sandbox environments safely.
    output_dir = '/tmp/edtech_output'
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, 'cleaned_logs.csv')
    
    clean_edtech_logs(input_csv, output_csv)
