"""
Session 03 — Set B: Healthcare Multi-Agent Swarm
Uses Google Genkit Python SDK with the Ollama plugin (llama3.2:1b).
Run with: genkit start -- python3 swarm.py
"""
import os
import asyncio
from pydantic import BaseModel, Field
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition

# ── Genkit initialisation with Ollama plugin ─────────────────────────────────
ai = Genkit(
    plugins=[
        Ollama(
            models=[ModelDefinition(name="llama3.2:1b")],
            server_address="http://localhost:11434",
        )
    ]
)

# ── Pydantic schemas ──────────────────────────────────────────────────────────
class SwarmInput(BaseModel):
    csv_data: str = Field(description="Raw CSV content from Session 01 scrubbed billing data")

class SwarmOutput(BaseModel):
    report: str = Field(description="Final Clinical Compliance Report")

# ── Helper: single agent call ─────────────────────────────────────────────────
async def call_agent(system_role: str, prompt: str) -> str:
    print(f"\n[Agent: {system_role}] processing...")
    response = await ai.generate(
        system=f"You are the {system_role}. Be concise, professional, and under 200 words.",
        prompt=prompt,
        model="ollama/llama3.2:1b",
    )
    return response.text.strip()

# ── Genkit Flow ───────────────────────────────────────────────────────────────
@ai.flow()
async def healthcare_agent_swarm(input_data: SwarmInput) -> SwarmOutput:
    print("Starting Healthcare Triple-Agent Swarm...")

    # 1. Clinical Analyst — identify billing violations
    analyst_out = await call_agent(
        "Clinical Analyst",
        f"Analyze this patient billing data:\n{input_data.csv_data[:1500]}\nFlag billing anomalies, negative amounts, and malformed ICD-10 codes.",
    )

    # 2. Compliance Auditor — validate against HIPAA/billing standards
    auditor_out = await call_agent(
        "Compliance Auditor",
        f"The Analyst found these violations:\n\n{analyst_out}\n\nAudit against HIPAA billing standards. Prioritize risk to patient data.",
    )

    # 3. Hospital Reporter — final clinical memo
    reporter_out = await call_agent(
        "Hospital Reporter",
        f"The Compliance Auditor found:\n\n{auditor_out}\n\nWrite a 2-paragraph professional Clinical Compliance Memo for hospital administration.",
    )

    print("\n--- Final Integrated Report ---")
    print(reporter_out)
    return SwarmOutput(report=reporter_out)


# ── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    input_file = "/tmp/healthcare_output/scrubbed_billing.csv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run Session 01 first.")
        return

    with open(input_file, "r") as f:
        csv_data = f.read()

    result = await healthcare_agent_swarm(SwarmInput(csv_data=csv_data))

    output_dir = "/tmp/healthcare_output"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "integrated_report.md"), "w") as f:
        f.write(result.report)
    print(f"\nReport saved to {output_dir}/integrated_report.md")


if __name__ == "__main__":
    ai.run_main(main())

