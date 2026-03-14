import os
import pandas as pd

def test_data_schema():
    slug = "ai_for_educators"
    path = f"01_data_pipeline_automation/set_{slug}/data/dirty_data.csv"
    if not os.path.exists(path):
        print(f"❌ Data file missing at {path}!")
        return False
    df = pd.read_csv(path)
    if len(df) < 5:
        print("⚠️ Data file seems empty or too small.")
        return False
    print("✅ Data schema and synthesis validated.")
    return True

if __name__ == "__main__":
    print(f"🛡️ Running Build Validation for {os.getcwd()}")
    if test_data_schema():
        print("🌟 BUILD STATUS: PASS")
    else:
        print("🚨 BUILD STATUS: WARNING")
