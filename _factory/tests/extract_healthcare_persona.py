import csv, json

with open("TeachMeAI Intake Responses - Intake_v2.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Row 100 — Doctor, healthcare provider, "Use ai for patient analysis"
row = rows[100]

print("=== ROW 100 FULL PROFILE ===")
print(f"Name: {row.get('Name')}")
print(f"Role: {row.get('Role Raw')}")
print(f"Role Category: {row.get('Role Category')}")
print(f"Goal: {row.get('Goal Short')}")
print(f"Digital Skills: {row.get('Digital Skills')}")
print(f"Skill Stage: {row.get('Skill Stage')}")
print(f"Status: {row.get('Status')}")
print()

json_cols = [
    "Intake State JSON",
    "Deep Research JSON",
    "Learner Profile JSON",
    "IMPACT Strategy JSON",
    "Execution Plan JSON",
    "Final Report JSON",
]

for col in json_cols:
    raw = row.get(col, "")
    print(f"=== {col} ===")
    if raw:
        try:
            d = json.loads(raw)
            print(json.dumps(d, indent=2)[:2000])
        except:
            print(f"(raw, not JSON): {raw[:500]}")
    else:
        print("(empty)")
    print()

# Also check rows 25, 60, 107 for comparison
for idx in [25, 60, 107]:
    r = rows[idx]
    print(f"--- Row {idx}: {r.get('Role Raw')} / {r.get('Role Category')} / Goal: {r.get('Goal Short')} ---")
    dr = r.get("Deep Research JSON", "")
    lp = r.get("Learner Profile JSON", "")
    if dr:
        try:
            d = json.loads(dr)
            print(f"  maturity: {d.get('marketMaturityScore')}, priorities: {len(d.get('topPriorities', []))}")
        except:
            print(f"  (parse failed)")
    if lp:
        try:
            l = json.loads(lp)
            print(f"  decisionStyle: {l.get('decisionStyle')}, cognitive: {l.get('cognitiveLoadTolerance')}")
        except:
            print(f"  (parse failed)")
    print()
