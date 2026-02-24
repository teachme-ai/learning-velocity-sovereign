"""
logic/genkit_audit_py/main.py — Sovereign Audit Committee
Session 03: Multi-Agent Systems — Firebase Genkit (Python SDK)

Three-agent sequential pipeline with full trace observability in the Genkit Dev UI.

Agents:
  1. Forensic Investigator  → structured ForensicReport (Pydantic)
  2. Risk Strategist        → structured StrategyDraft  (Pydantic)
  3. Executive Critic       → structured CriticOutput   (Pydantic, retry loop ≥2 weaknesses)

Run:
  pip install -r requirements.txt
  genkit start -- python3 main.py        # opens Dev UI at http://localhost:4000
  genkit flow:run auditCommitteeFlow '{"csv_data": "..."}'  # CLI run
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from genkit.ai import Genkit
from genkit.blocks.interfaces import Output
from genkit.plugins.google_genai import GoogleAI

# ── Initialise ────────────────────────────────────────────────────────────────

ai = Genkit(
    plugins=[GoogleAI()],                  # reads GEMINI_API_KEY from env
    model='googleai/gemini-2.5-flash',
)

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR  = Path(__file__).resolve().parent.parent.parent  # 03_multi_agent_systems/
INPUT_CSV = (
    BASE_DIR.parent
    / '01_data_pipeline_automation'
    / 'data'
    / 'flagged_expenses.csv'
)


# ── Pydantic Schemas ──────────────────────────────────────────────────────────

class AuditInput(BaseModel):
    csv_data: str = Field(description='Contents of flagged_expenses.csv as plain text')


class Violation(BaseModel):
    transaction_id: str  = Field(description='Transaction reference ID')
    rule_broken:    str  = Field(description='Exact policy rule violated')
    severity:       Literal['HIGH', 'MEDIUM', 'LOW']
    approval_issue: str  = Field(description='Finding on the approval chain')


class ForensicReport(BaseModel):
    violations: list[Violation] = Field(description='All identified policy violations')
    summary:    str             = Field(description='Overall forensic assessment')


class StrategyDraft(BaseModel):
    risk_rating:               Literal['CRITICAL', 'HIGH', 'MODERATE', 'LOW']
    total_exposure_usd:        float = Field(description='Total financial exposure in USD')
    quarterly_budget_impact_pct: float = Field(description='Percentage of quarterly budget at risk')
    mitigations:               list[str] = Field(description='Three concrete mitigation strategies')


class CriticOutput(BaseModel):
    weaknesses:       list[str] = Field(min_length=2, description='At least two identified weaknesses')
    revised_strategy: str       = Field(description='Improved strategy fixing all weaknesses')


class CommitteeReport(BaseModel):
    forensic_report: ForensicReport
    strategy_draft:  StrategyDraft
    critic_feedback: CriticOutput


# ── System Prompts ─────────────────────────────────────────────────────────────

FORENSIC_SYSTEM = (
    'You are the Forensic Investigator on the Sovereign Audit Committee. '
    'Analyze raw expense data and identify SPECIFIC policy violations. '
    'For each flagged transaction: state the exact rule broken, assign severity '
    '(HIGH/MEDIUM/LOW), and assess the approval chain. Be exhaustive.'
)

STRATEGIST_SYSTEM = (
    'You are the Risk Strategist on the Sovereign Audit Committee. '
    'Receive forensic findings and assess FINANCIAL IMPACT on the quarterly budget. '
    'Quantify total exposure, percentage of budget at risk, assign a Risk Rating, '
    'and propose exactly three mitigation strategies.'
)

CRITIC_SYSTEM = (
    'You are the Executive Critic on the Sovereign Audit Committee. '
    'Your role is QUALITY CONTROL — you must be demanding and rigorous. '
    'You MUST identify AT LEAST TWO specific weaknesses in the strategy presented '
    'and provide a REVISED strategy that addresses each one. '
    'This is your mandate — never approve without revision.'
)


# ── Main Flow ─────────────────────────────────────────────────────────────────

@ai.flow()
async def auditCommitteeFlow(input_data: AuditInput) -> CommitteeReport:
    """
    Orchestrates the three-agent audit deliberation.
    Each ai.generate() call is individually traced in the Genkit Developer UI.
    """

    # ── Agent 1: Forensic Investigator ────────────────────────────────────────
    print('\n═══ Agent 1: Forensic Investigator deliberating... ═══')
    forensic_result = await ai.generate(
        prompt=(
            f'Analyze these flagged transactions for policy violations:\n\n'
            f'{input_data.csv_data}\n\n'
            f'Return exhaustive findings as structured JSON.'
        ),
        system=FORENSIC_SYSTEM,
        output=Output(schema=ForensicReport),
        config={'temperature': 0.3},
    )
    forensic_report: ForensicReport = forensic_result.output
    print(f'[Forensic] Found {len(forensic_report.violations)} violations.')
    print(f'[Forensic] Summary: {forensic_report.summary}')

    # ── Agent 2: Risk Strategist ───────────────────────────────────────────────
    print('\n═══ Agent 2: Risk Strategist deliberating... ═══')
    strategy_result = await ai.generate(
        prompt=(
            f'The Forensic Investigator produced these findings:\n\n'
            f'{forensic_report.model_dump_json(indent=2)}\n\n'
            f'Assess the financial impact and propose three mitigation strategies.'
        ),
        system=STRATEGIST_SYSTEM,
        output=Output(schema=StrategyDraft),
        config={'temperature': 0.4},
    )
    strategy_draft: StrategyDraft = strategy_result.output
    print(f'[Strategist] Risk Rating: {strategy_draft.risk_rating}')
    print(f'[Strategist] Exposure: ${strategy_draft.total_exposure_usd:,.0f}')

    # ── Agent 3: Executive Critic (retry loop) ─────────────────────────────────
    print('\n═══ Agent 3: Executive Critic reviewing... ═══')
    MAX_RETRIES = 3
    critic_output: CriticOutput | None = None

    for attempt in range(1, MAX_RETRIES + 1):
        print(f'[Critic] Review attempt {attempt}/{MAX_RETRIES}...')
        critic_result = await ai.generate(
            prompt=(
                f'The Risk Strategist produced this analysis:\n\n'
                f'{strategy_draft.model_dump_json(indent=2)}\n\n'
                f'Find AT LEAST TWO weaknesses and produce a revised strategy.'
            ),
            system=CRITIC_SYSTEM,
            output=Output(schema=CriticOutput),
            config={'temperature': 0.6},
        )
        candidate: CriticOutput = critic_result.output

        if len(candidate.weaknesses) >= 2:
            critic_output = candidate
            print(f'[Critic] ✅ Quality gate passed with {len(candidate.weaknesses)} weaknesses.')
            for i, w in enumerate(candidate.weaknesses, 1):
                print(f'  [WEAKNESS {i}] {w}')
            break
        else:
            print(f'[Critic] ⚠️  Only {len(candidate.weaknesses)} weakness — retrying...')

    if critic_output is None:
        raise RuntimeError(
            f'Executive Critic failed to find ≥2 weaknesses after {MAX_RETRIES} attempts.'
        )

    print('\n═══ Committee deliberation complete. ═══')
    return CommitteeReport(
        forensic_report=forensic_report,
        strategy_draft=strategy_draft,
        critic_feedback=critic_output,
    )


# ── CLI entry point ───────────────────────────────────────────────────────────

async def main() -> None:
    if not INPUT_CSV.exists():
        print(f'[ERROR] Input CSV not found: {INPUT_CSV}')
        print('  Run Session 01 cleaner.py first.')
        return

    csv_data = INPUT_CSV.read_text(encoding='utf-8')
    print(f'[INFO]  Loaded {INPUT_CSV.name}')
    print(f'[INFO]  Launching Sovereign Audit Committee...\n')

    report = await auditCommitteeFlow(AuditInput(csv_data=csv_data))

    # Save output
    output_path = BASE_DIR / 'data' / 'genkit_committee_report.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report.model_dump(), indent=2),
        encoding='utf-8',
    )
    print(f'\n[INFO]  Full report saved → {output_path}')


ai.run_main(main())
