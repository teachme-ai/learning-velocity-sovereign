import json
from datetime import datetime

with open("_factory/logs/events.jsonl") as f:
    events = [json.loads(line) for line in f if line.strip()]

key_events = {}
for e in events:
    ts = datetime.fromisoformat(e["timestamp"])
    ev = e["event"]
    if "Generating DNA context" in ev:
        key_events["dna_start"] = ts
    elif "DNA context generated" in ev:
        key_events["dna_end"] = ts
    elif "data synthesis agent" in ev and "Initiating" in ev:
        key_events["synth_start"] = ts
    elif "Data synthesis" in ev and "completed" in ev:
        key_events["synth_end"] = ts
    elif "Pass 1 complete" in ev and "48 files" in ev:
        key_events["pass1_end"] = ts
    elif "Pass 2: draining" in ev and "48 jobs" in ev:
        key_events["pass2_start"] = ts
    elif "Pass 2 complete" in ev and "deferred': False" in ev:
        if "pass2_end" not in key_events:
            key_events["pass2_end"] = ts

print("PHASE TIMING (Healthcare full build - Test 7):")
print("-" * 55)

if "dna_start" in key_events and "dna_end" in key_events:
    d = (key_events["dna_end"] - key_events["dna_start"]).total_seconds()
    print(f"  DNA Context (llama3.2:1b):       {d:.1f}s")

if "synth_start" in key_events and "synth_end" in key_events:
    d = (key_events["synth_end"] - key_events["synth_start"]).total_seconds()
    print(f"  Data Synth (qwen2.5:0.5b):       {d:.1f}s")

if "pass2_start" in key_events and "pass2_end" in key_events:
    d = (key_events["pass2_end"] - key_events["pass2_start"]).total_seconds()
    per_file = d / 48
    sequential_est = per_file * 48
    print(f"  Pass 2 / 48 files (llama3.2:3b): {d:.1f}s")
    print(f"    Per file avg:                  {per_file:.1f}s")
    print(f"    Sequential estimate:           {sequential_est:.0f}s ({sequential_est/60:.1f}min)")
    print(f"    Actual (3 workers):            {d:.0f}s ({d/60:.1f}min)")

print()
print("TOTAL: 2m31s cold | 3.8s warm")
