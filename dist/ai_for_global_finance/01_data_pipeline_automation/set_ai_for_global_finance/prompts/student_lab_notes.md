## Student Lab Notes — Session 01
### Introduction to AI for Global Finance and Data Integrity

---

> **Core Principle:** _An LLM is only as trustworthy as the data you feed it. Garbage in, garbage out — at enterprise scale._

---

## The Problem: The Dark Side of Large Language Models in Compliance Pipelines

Large Language Models (LLMs) have revolutionized various industries by providing accurate and insightful responses to user queries. However, their potential for abuse and misuse is a significant concern in compliance pipelines where incorrect categorizations can result in substantial financial losses.

### Example of the Failure Mode:

| Input sent to LLM | LLM Response | Reality |
|---|---|---|
| `amount_usd: "N/A"` | `"Policy-Compliant — routine expense"` | The field was broken |
| `description: " "` | `"Needs Review — insufficient detail"` | The row was corrupt |
| `amount_usd: -450.00` | `"Policy-Compliant — small credit"` | Invalid negative value |

The LLM gave a confident, formatted answer every time — and was wrong every time.

---

## The Solution: Pydantic as the Gatekeeper for Data Integrity

Pydantic serves as an effective **data gatekeeper** that ensures data integrity before it reaches the LLM. It acts as a strict contract enforcement mechanism on your data, providing a standardized and auditable interface to validate input before passing it to the LLM.

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

### [INTEGRATOR] Perspective
You are integrating two systems that have **different failure modes**:

- **Rules** fail loudly — a Pydantic `ValidationError` crashes immediately and tells you exactly what is wrong.
- **LLMs** fail silently — a miscategorization looks like a valid response.

By running rules _first_, you guarantee that the LLM only ever receives well-formed data. The LLM's job is then purely interpretive — it handles ambiguity with nuance and accuracy.

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

In an enterprise context, you may be running models **on-premises** (using Ollama instead of a cloud API). The integration requirements differ from those in traditional environments due to constraints such as limited scalability and security considerations. Implementing these best practices ensures that data is properly validated before being fed into the AI system.

### Key Takeaways:

- Use Pydantic as a gatekeeper for your data.
- Ensure robust validation of input data before feeding it into any system, including LLMs.
- Consider hybrid approaches where rules and LLMs are used in tandem to maximize accuracy while minimizing false positives.