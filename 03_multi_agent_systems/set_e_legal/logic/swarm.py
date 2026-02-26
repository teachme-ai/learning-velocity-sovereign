"""
Session 03 — Set E: Legal Multi-Agent Swarm
Uses Google Genkit Python SDK with the Ollama plugin (llama3.2:1b).
Run with: genkit start -- python3 swarm.py
"""
import os
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
    json_data: str = Field(description="JSON string from Session 01 scanned_clauses.json")

class SwarmOutput(BaseModel):
    report: str = Field(description="Final Contract Due Diligence Brief")

# ── Helper: single agent call ─────────────────────────────────────────────────
async def call_agent(system_role: str, prompt: str) -> str:
    print(f"\n[Agent: {system_role}] processing...")
    response = await ai.generate(
        system=f"You are the {system_role}. Be concise, analytical, and under 200 words.",
        prompt=prompt,
        model="ollama/llama3.2:1b",
    )
    return response.text.strip()

# ── Genkit Flow ───────────────────────────────────────────────────────────────
@ai.flow()
async def legal_agent_swarm(input_data: SwarmInput) -> SwarmOutput:
    print("Starting Legal Triple-Agent Swarm...")

    # 1. Paralegal Agent — summarise high-risk clauses
    analyst_out = await call_agent(
        "Paralegal Agent",
        f"Analyze this risk-mapped contract data:\n{input_data.json_data[:1500]}\nSummarise the HIGH and MEDIUM liability markers found.",
    )

    # 2. Compliance Auditor — cross-check against M&A law standards
    auditor_out = await call_agent(
        "Compliance Auditor",
        f"The Paralegal flagged these liability markers:\n\n{analyst_out}\n\nCross-check against standard M&A law. State the operational risk level.",
    )

    # 3. Counsel Reporter — urgent summary for the Legal Board
    reporter_out = await call_agent(
        "Counsel Reporter",
        f"Based on the Compliance Auditor's findings:\n\n{auditor_out}\n\nWrite a 2-paragraph Contract Due Diligence Brief recommending renegotiation actions.",
    )

    print("\n--- Final Integrated Report ---")
    print(reporter_out)
    return SwarmOutput(report=reporter_out)


# ── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    input_file = "/tmp/legal_output/scanned_clauses.json"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run Session 01 first.")
        return

    with open(input_file, "r") as f:
        json_data = f.read()

    result = await legal_agent_swarm(SwarmInput(json_data=json_data))

    output_dir = "/tmp/legal_output"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "integrated_report.md"), "w") as f:
        f.write(result.report)
    print(f"\nReport saved to {output_dir}/integrated_report.md")


if __name__ == "__main__":
    ai.run_main(main())

