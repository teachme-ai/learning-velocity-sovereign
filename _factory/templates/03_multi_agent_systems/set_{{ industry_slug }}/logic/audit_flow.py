"""
audit_flow.py — Refined Sovereign Audit Committee
Session 03: Multi-Agent Systems — Firebase Genkit (Python SDK)

This script demonstrates orchestrating specialized agents in a type-safe flow 
with automated quality checks.

Workflow:
  1. forensic_analyzer -> JSON list of violations
  2. risk_strategist   -> Markdown risk summary
  3. executive_critic   -> Professional Tone & Actionable Advice check

Run:
  export GEMINI_API_KEY='your-key'
  python audit_flow.py
"""

from __future__ import annotations
import os
import json
from typing import List
from pydantic import BaseModel, Field
from genkit.ai import Genkit
from genkit.blocks.interfaces import Output
from genkit.plugins.google_genai import GoogleAI

# 1. Initialize Genkit
genkit = Genkit(
    plugins=[GoogleAI()],
    model='googleai/gemini-2.5-flash',
)

# 2. Define Data Schemas
class Violation(BaseModel):
    transaction_id: str = Field(description='Transaction ID')
    rule_broken: str = Field(description='The specific policy rule that was violated')
    severity: str = Field(description='HIGH, MEDIUM, or LOW')
    approval_issue: str = Field(description='Analysis of the approval chain')

class ForensicReport(BaseModel):
    violations: List[Violation] = Field(description='JSON list of identified violations')

class CriticOutput(BaseModel):
    tone_evaluation: str = Field(description='Check for Professional Tone')
    advice_evaluation: str = Field(description='Check for Actionable Advice')
    critique: str = Field(description='Specific feedback for the Strategist')
    final_report: str = Field(description='The final approved or revised Markdown report')

# 3. Define Orchestration Flow
@genkit.flow(name="auditCommitteeFlow")
async def audit_flow(csv_data: str) -> str:
    print("\n[STEP 1] Forensic Investigator analyzing data...")
    forensic_result = await genkit.generate(
        system="You are a Forensic Investigator. Identify expense policy violations. Output a JSON list.",
        prompt=f"Transactions:\n{csv_data}",
        output=Output(schema=ForensicReport)
    )
    findings: ForensicReport = forensic_result.output
    print(f" [OK] Found {len(findings.violations)} violations.")

    print("\n[STEP 2] Risk Strategist drafting summary...")
    strategy_result = await genkit.generate(
        system="You are a Risk Strategist. Consume the JSON violations and output a professional Markdown summary.",
        prompt=findings.model_dump_json(indent=2)
    )
    markdown_report: str = strategy_result.text
    print(" [OK] Strategy draft complete.")

    print("\n[STEP 3] Executive Critic reviewing report...")
    critic_result = await genkit.generate(
        system=(
            "You are an Executive Critic. Review the Markdown for 'Professional Tone' and 'Actionable Advice'. "
            "Return evaluations and the final revised report."
        ),
        prompt=markdown_report,
        output=Output(schema=CriticOutput)
    )
    final_results: CriticOutput = critic_result.output
    print(f" [OK] Tone: {final_results.tone_evaluation}")
    print(f" [OK] Advice: {final_results.advice_evaluation}")
    
    return final_results.final_report

# 4. Entry Point
async def main():
    sample_data = (
        "transaction_id,amount_usd,approved_by,description\n"
        "TXN-001,15000,mgr-ali,Server hosting\n"
        "TXN-002,2500,dir-faisal,Office supplies\n"
        "TXN-003,45000,vp-jane,International Relocation"
    )
    print("\n--- Starting Sovereign Audit Committee ---")
    final_report = await audit_flow(sample_data)
    print("\n--- Final Approved Boardroom Report ---\n")
    print(final_report)

if __name__ == "__main__":
    os.environ['GENKIT_ENV'] = 'dev'
    genkit.run_main(main())
