import os
import pandas as pd

def test_data_schema():
    path = "01_data_pipeline_automation/set_sustainability_and_esg/data/corporate_expenses.csv"
    if not os.path.exists(path):
        print("❌ Data file missing!")
        return False
    df = pd.read_csv(path)
    expected_cols = ['transaction_id', 'date', 'employee_id', 'department', 'category', 'description', 'amount_usd']
    # Check if a subset of columns exist (since synth might be slightly off)
    actual_cols = df.columns.tolist()
    missing = [c for c in expected_cols if c not in actual_cols]
    if missing:
        print(f"⚠️ Missing columns: {missing}")
        return False
    print("✅ Data schema validated.")
    return True

def test_sessions_exist():
    sessions = ['01_data_pipeline_automation', '07_sovereign_security', '08_grand_capstone']
    for s in sessions:
        if not os.path.exists(s):
            print(f"❌ Session {s} folder missing!")
            return False
    print("✅ Session structure validated.")
    return True

if __name__ == "__main__":
    print(f"🛡️ Running Build Validation for {os.getcwd()}")
    s1 = test_data_schema()
    s2 = test_sessions_exist()
    if s1 and s2:
        print("🌟 BUILD STATUS: PASS")
    else:
        print("🚨 BUILD STATUS: WARNING (Incomplete or schema mismatch)")
