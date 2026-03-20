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
In a healthcare enterprise, especially when dealing with Protected Health Information (PHI) or sensitive research data, operating AI models **on-premises** (e.g., deploying an LLM for clinical note summarization via Ollama rather than a public cloud API) is often a non-negotiable requirement. This approach provides critical operational advantages:

1.  **Data never leaves your infrastructure** — For healthcare organizations, data sovereignty is paramount. Running models on-premises guarantees that Protected Health Information (PHI), patient records, or proprietary research data never egresses your controlled network boundaries. Pydantic validation acts as an essential pre-inference gatekeeper, ensuring only schema-compliant, de-identified (if applicable), and correctly structured data—say, patient demographics or lab results—is even presented to the AI model, preventing accidental exposure of malformed or sensitive raw inputs.

2.  **Audit trails are complete** — Robust auditability is critical for regulatory compliance (e.g., HIPAA, GDPR, FDA 21 CFR Part 11) and clinical governance. Every piece of input data—be it a patient's diagnostic imaging report or a clinician's free-text note—is meticulously logged. If Pydantic validation identifies a malformed record or a missing critical field, that "rejected row" is logged with a specific, traceable reason _before_ any AI inference occurs. This provides an irrefutable trail for incident investigations, compliance audits, and understanding data quality issues impacting AI model performance in a clinical setting.

3.  **Reproducibility** — In healthcare AI, particularly for diagnostic support or risk stratification, the ability to reproduce results is vital for clinical validation, model explainability, and safety. Rule-based flags—for instance, flagging a patient based on specific lab values or medication contraindications—are 100% deterministic and can be re-run identically, providing predictable, auditable outcomes. While LLM results (e.g., summarizing a patient's medical history) are inherently probabilistic, their outputs are significantly bounded and made more reliable by the preceding validated inputs. This deterministic pre-processing step improves the overall interpretability and safety profile of the AI system, allowing clinicians to trace potential issues back to well-defined data inputs rather than ambiguous model behavior.
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