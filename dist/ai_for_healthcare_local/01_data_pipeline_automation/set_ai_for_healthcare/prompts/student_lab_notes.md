# Student Lab Notes — Session 01
## The Data Integrity Lesson: Why Pydantic Comes Before the LLM

---

> **Core Principle:** _An LLM is only as trustworthy as the data you feed it. Garbage in, garbage out — at enterprise scale._

---

## The Problem: LLMs Are Optimistic

Large Language Models are trained to be helpful. When you send them messy, malformed, or ambiguous data, they do not crash — they **hallucinate a plausible answer**. This is catastrophic in a compliance pipeline where a wrong category (`Policy-Compliant` instead of `Suspicious`) can cost an enterprise millions.

### Example of the failure mode:

| Input sent to LLM | LLM Response | Reality |
|---|---|---|
| `amount_usd: "N/A"` | `"Policy-Compliant — routine expense"` | The field was broken |
| `description: " "` | `"Needs Review — insufficient detail"` | The row was corrupt |
| `amount_usd: -450.00` | `"Policy-Compliant — small credit"` | Invalid negative value |

The LLM gave a confident, formatted answer every time — and was wrong every time.

---

## The Solution: Pydantic as the Gatekeeper

Pydantic enforces a **strict contract** on your data _before_ it touches the LLM. Think of it as a bouncer at the door of your AI system.

```
RAW CSV DATA
     │
     ▼
┌─────────────────────────────┐
│   Pydantic Schema Guard     │  ← Phase 1: Deterministic
│                             │
│  ✅ Type coercion           │
│  ✅ Required field checks   │
│  ✅ Validator logic         │
│  ✅ Threshold rules         │
└──────────────┬──────────────┘
               │  Only clean, validated rows pass
               ▼
┌─────────────────────────────┐
│   Ollama LLM  (llama3.2)    │  ← Phase 2: Probabilistic
│                             │
│  🧠 Description → Category  │
│  🧠 Context-aware reasoning │
│  🧠 Nuanced edge cases      │
└─────────────────────────────┘
               │
               ▼
       HYBRID AUDIT REPORT
```

---

## The Two-Phase Architecture

### [BUILDER] Perspective
You are integrating two systems that have **different failure modes**:

- **Rules** fail loudly — a Pydantic `ValidationError` crashes immediately and tells you exactly what is wrong.
- **LLMs** fail silently — a miscategorisation looks like a valid response.

By running rules _first_, you guarantee that the LLM only ever receives well-formed data. The LLM's job is then purely interpretive — it handles the ambiguity that rules cannot.

### [ARCHITECT] Perspective
This is the **Defence in Depth** pattern applied to AI pipelines:

| Layer | Tool | Type | Failure Mode |
|---|---|---|---|
| Layer 1 | Pydantic | Deterministic | Loud (exception) |
| Layer 2 | Threshold Rule | Deterministic | Loud (conditional) |
| Layer 3 | Ollama LLM | Probabilistic | Silent (needs logging) |

Each layer catches what the previous layer cannot. No single layer is trusted alone.

---

## Why This Matters for Sovereign AI
In an enterprise context, you're running models on-premises with Ollama, utilizing a private cloud infrastructure that secures sensitive patient data. This means:

1. **Data remains within your HIPAA-compliant environment** — Pydantic validation ensures only schema-clean data is even processed, reducing the risk of EHR breaches.
2. **Audit trails are complete and compliant** — every rejected row is logged with a specific reason _before_ any AI inference occurs, satisfying audit trail requirements for regulatory compliance.
3. **Reproducibility and consistency** — rule-based flags are 100% deterministic, leveraging validated inputs to ensure LLM results are probabilistic yet bounded within a secure and auditable framework.
## Key Takeaways

- ✅ **Always validate before you infer.** Pydantic is your data contract.
- ✅ **Deterministic rules catch known bad patterns.** LLMs catch unknown, nuanced ones.
- ✅ **A hybrid pipeline is more robust than either approach alone.**
- ✅ **Silent AI failures are more dangerous than loud rule failures.**

---

## Hands-On Check

Before moving to Session 02, confirm you can answer:

1. What happens if you send a row with a missing `transaction_id` directly to the LLM?
2. Why does `amount_usd` need to be coerced to `float` _before_ Pydantic validation?
3. What is the risk of using _only_ the LLM without the threshold rule?

---

_Session 01 · AI Bootcamps · Sovereign Data Pipeline_
_Persona: Supportive Facilitator · Theme: Cyber-Sovereign_