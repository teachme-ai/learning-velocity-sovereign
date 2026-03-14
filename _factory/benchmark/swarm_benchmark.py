"""
Swarm Agent Benchmark — Model Head-to-Head
Tests llama3.2:1b vs available models on the real 3-agent chain.
Task: Financial Analyst → Corporate Auditor → Executive Reporter
"""

import ollama
import time
import textwrap

# ── Sample corporate expense data (mirrors what the swarm actually processes) ──
CSV_DATA = """
employee,department,amount,category,policy_limit,flag
Sarah Chen,Sales,4200.00,International Travel,3000.00,OVER_LIMIT
Marcus Williams,IT,890.50,Software Licenses,500.00,OVER_LIMIT
Jennifer Torres,Finance,1200.00,Team Entertainment,800.00,OVER_LIMIT
David Kim,Operations,2800.00,Conference & Training,2000.00,OVER_LIMIT
Amanda Foster,HR,340.00,Office Supplies,500.00,NO_RECEIPT
Robert Patel,Sales,5500.00,Client Entertainment,4000.00,OVER_LIMIT
Lisa Johnson,Marketing,1800.00,Advertising,2000.00,SPLIT_PAYMENT
Michael Brown,Legal,3200.00,External Counsel,3000.00,OVER_LIMIT
""".strip()

# ── Agent prompts (identical to swarm.py) ─────────────────────────────────────
AGENTS = [
    {
        "role": "Financial Analyst",
        "system": "You are the Financial Analyst. Be concise, professional, and under 200 words.",
        "prompt_template": "Identify all out-of-bounds expenses from this data:\n{input}\nProvide a concise bulleted list of violations.",
    },
    {
        "role": "Corporate Auditor",
        "system": "You are the Corporate Auditor. Be concise, professional, and under 200 words.",
        "prompt_template": "Review these Analyst findings:\n\n{input}\n\nCheck against Corporate Travel Policy. Prioritize high-risk findings.",
    },
    {
        "role": "Executive Reporter",
        "system": "You are the Executive Reporter. Be concise, professional, and under 200 words.",
        "prompt_template": "The Auditor provided:\n\n{input}\n\nWrite a 2-paragraph professional Corporate Investigation Memo summarizing the risks.",
    },
]

MODELS = [
    "llama3.2:1b",
    "llama3.2:latest",   # 3.2B
    "gemma3n:e2b",       # 4.5B
    "deepseek-r1:8b",    # 8.2B reasoning
]

DIVIDER = "=" * 70


def run_agent(model: str, system: str, prompt: str) -> tuple[str, float]:
    t0 = time.time()
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    )
    elapsed = time.time() - t0
    return response["message"]["content"].strip(), elapsed


def run_swarm(model: str) -> dict:
    print(f"\n  Running agent chain...")
    chain_input = CSV_DATA
    timings = []
    outputs = []

    for agent in AGENTS:
        prompt = agent["prompt_template"].format(input=chain_input)
        output, t = run_agent(model, agent["system"], prompt)
        timings.append(t)
        outputs.append(output)
        chain_input = output  # feed into next agent
        print(f"    [{agent['role']}] done in {t:.1f}s")

    return {
        "analyst": outputs[0],
        "auditor": outputs[1],
        "memo": outputs[2],
        "total_time": sum(timings),
        "timings": timings,
    }


def score_memo(memo: str) -> dict:
    """Simple heuristic scoring of the final executive memo."""
    text = memo.lower()
    scores = {
        "length_ok":        50 <= len(memo.split()) <= 300,
        "two_paragraphs":   memo.count("\n\n") >= 1 or memo.count("\n") >= 3,
        "names_specific":   any(n.lower() in text for n in ["sarah", "marcus", "patel", "robert", "jennifer"]),
        "risk_language":    any(w in text for w in ["risk", "violation", "policy", "compliance", "immediate"]),
        "dollar_amounts":   "$" in memo or any(c.isdigit() for c in memo),
        "action_oriented":  any(w in text for w in ["recommend", "action", "require", "must", "should", "review"]),
    }
    score = sum(scores.values())
    return {"score": score, "max": len(scores), "detail": scores}


def print_result(model: str, result: dict):
    sc = score_memo(result["memo"])
    bar = "█" * sc["score"] + "░" * (sc["max"] - sc["score"])

    print(f"\n{DIVIDER}")
    print(f"  MODEL : {model}")
    print(f"  TIME  : {result['total_time']:.1f}s total  "
          f"(analyst {result['timings'][0]:.1f}s | "
          f"auditor {result['timings'][1]:.1f}s | "
          f"reporter {result['timings'][2]:.1f}s)")
    print(f"  SCORE : [{bar}] {sc['score']}/{sc['max']}")
    print(f"  DETAIL: {sc['detail']}")
    print(f"\n  --- ANALYST OUTPUT ---")
    print(textwrap.indent(result["analyst"][:600], "  "))
    print(f"\n  --- FINAL MEMO ---")
    print(textwrap.indent(result["memo"][:800], "  "))
    print(DIVIDER)


def main():
    print(f"\n{'#' * 70}")
    print("  SWARM BENCHMARK: 3-Agent Chain (Financial Analyst → Auditor → Reporter)")
    print(f"  Task: Corporate expense audit on {len(CSV_DATA.splitlines())} transactions")
    print(f"  Models: {', '.join(MODELS)}")
    print(f"{'#' * 70}")

    all_results = {}
    for model in MODELS:
        print(f"\n▶ {model}")
        try:
            result = run_swarm(model)
            all_results[model] = result
            print_result(model, result)
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            all_results[model] = None

    # ── Final comparison table ─────────────────────────────────────────────
    print(f"\n\n{'#' * 70}")
    print("  FINAL COMPARISON")
    print(f"{'#' * 70}")
    print(f"\n  {'Model':<22} {'Time':>8} {'Score':>8}  {'Verdict'}")
    print(f"  {'-'*22} {'-'*8} {'-'*8}  {'-'*20}")

    scored = []
    for model, r in all_results.items():
        if r:
            sc = score_memo(r["memo"])
            scored.append((model, r["total_time"], sc["score"], sc["max"]))

    scored.sort(key=lambda x: (-x[2], x[1]))  # best score first, then fastest

    for i, (model, t, score, mx) in enumerate(scored):
        verdict = "⭐ RECOMMENDED" if i == 0 else ("✅ Good" if score >= mx * 0.7 else "⚠️  Weak")
        print(f"  {model:<22} {t:>7.1f}s {score:>5}/{mx}    {verdict}")

    print()


if __name__ == "__main__":
    main()
