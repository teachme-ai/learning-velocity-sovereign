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
In the healthcare enterprise, deploying AI models **on-premises** (leveraging tools like Ollama instead of a cloud API) is more than a technical choice; it's a strategic imperative for managing sensitive patient information and proprietary research. This operational model ensures:

1.  **Unwavering Data Governance:** Patient data, clinical trial results, and proprietary research insights remain strictly within your organizational infrastructure. Pydantic validation acts as the critical first line of defense, ensuring only schema-clean data—such as properly formatted EHR entries, lab results, or medical imaging metadata—is ever processed by the AI. This is fundamental for HIPAA compliance, GDPR adherence, and maintaining the integrity of protected health information (PHI) and institutional IP.
2.  **Comprehensive Accountability & Traceability:** Every data point rejected by the system is meticulously logged with a specific, actionable reason *before* any AI inference occurs. This provides an exhaustive audit trail, essential for regulatory compliance (e.g., FDA, CQC), internal clinical governance, and incident investigation. You can precisely trace why a malformed patient record, an out-of-range lab value, or an incomplete diagnostic code was excluded from AI processing, demonstrating due diligence.
3.  **Clinical Reproducibility & Risk Mitigation:** For critical clinical applications, the ability to re-run an analysis identically is paramount. Rule-based flags, such as those identifying potential adverse drug events or specific diagnostic criteria, are 100% deterministic and can be reproduced precisely. While LLM results are inherently probabilistic, their outputs are significantly bounded and contextualized by the validated inputs. This offers a controlled environment for their application in areas like clinical note summarization or literature review, where input integrity is key to managing interpretational risk and ensuring a reliable foundation for human review.
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