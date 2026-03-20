import pandas as pd
import re
import os

def scrub_pii(df):
    """Simple regex-based PII scrubber for names and emails."""
    print("🛡️ Scrubbing PII from dataset...")
    
    # Mask emails
    if 'email' in df.columns:
        df['email'] = df['email'].apply(lambda x: "REDACTED@ai_for_healthcare.com" if pd.notnull(x) else x)
    
    # Mask names (simple approach for the lab)
    if 'employee_id' in df.columns:
        df['employee_id'] = df['employee_id'].apply(lambda x: f"USER_{x[-3:]}" if pd.notnull(x) and len(str(x)) > 3 else "USER_HIDDEN")
    
    return df

if __name__ == "__main__":
    data_path = "data/dirty_data.csv"
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        scrubbed_df = scrub_pii(df)
        scrubbed_df.to_csv("data/scrubbed_data.csv", index=False)
        print("✅ PII Scrubbing complete. Saved to data/scrubbed_data.csv")
    else:
        print(f"❌ Data file {data_path} not found.")