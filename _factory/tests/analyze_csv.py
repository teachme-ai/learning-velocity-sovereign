import csv, json

with open("TeachMeAI Intake Responses - Intake_v2.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Search for healthcare/medical roles
print("=== HEALTHCARE/MEDICAL ROWS ===")
found = False
for i, row in enumerate(rows):
    role = row.get("Role Raw", "").lower()
    role_cat = row.get("Role Category", "").lower()
    goal = row.get("Goal Short", "").lower()
    if any(kw in role + role_cat + goal for kw in ["health", "medical", "doctor", "clinic", "pharma", "nurse", "patient"]):
        found = True
        print(f"Row {i}: Role={row.get('Role Raw')} | Cat={row.get('Role Category')} | Goal={row.get('Goal Short')} | Digital={row.get('Digital Skills')} | Tech={row.get('Tech Savviness')}")

if not found:
    print("No healthcare-specific rows found.")

print()
print("=== ALL UNIQUE ROLE CATEGORIES ===")
cats = set()
for row in rows:
    c = row.get("Role Category", "").strip()
    if c:
        cats.add(c)
for c in sorted(cats):
    print(f"  {c}")

print()
print("=== LAST COMPLETE ROW (128) DEEP RESEARCH ===")
row = rows[128]
print(f"Name: {row.get('Name', 'N/A')}")
print(f"Role: {row.get('Role Raw', 'N/A')}")
print(f"Role Category: {row.get('Role Category', 'N/A')}")
print(f"Goal: {row.get('Goal Short', 'N/A')}")
print(f"Digital Skills: {row.get('Digital Skills', 'N/A')}")
print(f"Tech Savviness: {row.get('Tech Savviness', 'N/A')}")
print(f"Skill Stage: {row.get('Skill Stage', 'N/A')}")

dr = row.get("Deep Research JSON", "")
if dr:
    try:
        d = json.loads(dr)
        print(f"marketMaturityScore: {d.get('marketMaturityScore')}")
        tp = d.get("topPriorities", [])
        print(f"topPriorities ({len(tp)}):")
        for p in tp[:5]:
            if isinstance(p, dict):
                print(f"  - {p.get('name')} | Artifact: {p.get('portfolioArtifact')}")
            else:
                print(f"  - {p}")
    except Exception as e:
        print(f"Parse error: {e}")
        print(dr[:300])

lp = row.get("Learner Profile JSON", "")
if lp:
    try:
        l = json.loads(lp)
        print(f"decisionStyle: {l.get('decisionStyle')}")
        print(f"uncertaintyHandling: {l.get('uncertaintyHandling')}")
        print(f"cognitiveLoadTolerance: {l.get('cognitiveLoadTolerance')}")
        print(f"socialEntanglement: {l.get('socialEntanglement')}")
    except Exception as e:
        print(f"Profile parse error: {e}")
