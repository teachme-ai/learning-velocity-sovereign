"""
Session 03 — Set A: Finance Multi-Agent Swarm
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
    csv_data: str = Field(description="Raw CSV content from Session 01 flagged expenses")

class SwarmOutput(BaseModel):
    report: str = Field(description="Final Corporate Investigation Memo")

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
async def finance_agent_swarm(input_data: SwarmInput) -> SwarmOutput:
    print("Starting Corporate Finance Triple-Agent Swarm...")

    # 1. Financial Analyst — find anomalies
    analyst_out = await call_agent(
        "Financial Analyst",
        f"Identify all out-of-bounds expenses from this data:\n{input_data.csv_data[:1500]}\nProvide a concise bulleted list of violations.",
    )

    # 2. Corporate Auditor — validate against policy
    auditor_out = await call_agent(
        "Corporate Auditor",
        f"Review these Analyst findings:\n\n{analyst_out}\n\nCheck against Corporate Travel Policy. Prioritize high-risk findings.",
    )

    # 3. Executive Reporter — final memo
    reporter_out = await call_agent(
        "Executive Reporter",
        f"The Auditor provided:\n\n{auditor_out}\n\nWrite a 2-paragraph professional Corporate Investigation Memo summarizing the risks.",
    )

    print("\n--- Final Integrated Report ---")
    print(reporter_out)
    return SwarmOutput(report=reporter_out)


# ── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    input_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../01_data_pipeline_automation/set_a_finance/data/flagged_expenses.csv")
    )
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run Session 01 first.")
        return

    with open(input_file, "r") as f:
        csv_data = f.read()

    result = await finance_agent_swarm(SwarmInput(csv_data=csv_data))

    output_dir = "/tmp/finance_output"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "integrated_report.md"), "w") as f:
        f.write(result.report)
    print(f"\nReport saved to {output_dir}/integrated_report.md")


if __name__ == "__main__":
    ai.run_main(main())

