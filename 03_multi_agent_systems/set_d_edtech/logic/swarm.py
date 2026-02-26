"""
Session 03 — Set D: EdTech Multi-Agent Swarm
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
    csv_data: str = Field(description="Raw CSV content from Session 01 cleaned student logs")

class SwarmOutput(BaseModel):
    report: str = Field(description="Final Learning Velocity Executive Brief")

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
async def edtech_agent_swarm(input_data: SwarmInput) -> SwarmOutput:
    print("Starting EdTech Triple-Agent Swarm...")

    # 1. Pedagogical Analyst — flag learning anomalies
    analyst_out = await call_agent(
        "Pedagogical Analyst",
        f"Analyze this student log data:\n{input_data.csv_data[:1500]}\nFlag students with impossible scores (>100) or negative time spent as data anomalies.",
    )

    # 2. Academic Auditor — validate against district academic integrity policy
    auditor_out = await call_agent(
        "Academic Auditor",
        f"The Analyst found these student anomalies:\n\n{analyst_out}\n\nAudit against Academic Integrity Policy. Determine whether these are LMS bugs or potential cheating.",
    )

    # 3. Faculty Reporter — executive brief on learning decay
    reporter_out = await call_agent(
        "Faculty Reporter",
        f"Based on the Auditor's review:\n\n{auditor_out}\n\nWrite a 2-paragraph professional Executive Brief on learning decay and LMS data integrity for the Faculty Board.",
    )

    print("\n--- Final Integrated Report ---")
    print(reporter_out)
    return SwarmOutput(report=reporter_out)


# ── Entrypoint ────────────────────────────────────────────────────────────────
async def main():
    input_file = "/tmp/edtech_output/cleaned_logs.csv"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run Session 01 first.")
        return

    with open(input_file, "r") as f:
        csv_data = f.read()

    result = await edtech_agent_swarm(SwarmInput(csv_data=csv_data))

    output_dir = "/tmp/edtech_output"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "integrated_report.md"), "w") as f:
        f.write(result.report)
    print(f"\nReport saved to {output_dir}/integrated_report.md")


if __name__ == "__main__":
    ai.run_main(main())

