"""
set_d_edtech/logic/cleaner.py — Student Assessment Audit Pipeline
Session 01: Data Pipeline Automation | Domain: EdTech

Two-phase approach:
  Phase 1 (Deterministic) — Pydantic schema: score range 0-100, valid course code, no future submissions.
  Phase 2 (Probabilistic) — Ollama LLM flags anomalous grades for academic integrity review.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

import ollama
import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator

# ── Config ────────────────────────────────────────────────────────────────────

OLLAMA_MODEL       = "llama3.2"
LOW_SCORE_THRESHOLD = 50.0
COURSE_CODE_PATTERN = re.compile(r"^[A-Z]{2,4}-[0-9]{3}$")

BASE_DIR   = Path(__file__).resolve().parent.parent
INPUT_CSV  = BASE_DIR / "data" / "student_assessments.csv"
OUTPUT_CSV = BASE_DIR / "data" / "flagged_assessments.csv"


# ── Phase 1: Pydantic Schema ──────────────────────────────────────────────────

class AssessmentRecord(BaseModel):
    student_id: str
    submission_date: str
    course_code: str
    score: float
    instructor_id: str

    @field_validator("score")
    @classmethod
    def score_must_be_valid(cls, v: float) -> float:
        if not (0 <= v <= 100):
            raise ValueError(f"score must be between 0 and 100 (got {v})")
        return v

    @field_validator("course_code")
    @classmethod
    def must_match_course_pattern(cls, v: str) -> str:
        if not v or not COURSE_CODE_PATTERN.match(v.strip()):
            raise ValueError(f"course_code '{v}' does not follow XX-000 pattern")
        return v.strip()

    @field_validator("submission_date")
    @classmethod
    def no_future_dates(cls, v: str) -> str:
        try:
            sub_date = date.fromisoformat(v)
            if sub_date > date.today():
                raise ValueError(f"submission_date '{v}' is in the future.")
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        return v


def load_and_validate(path: Path) -> tuple[list[dict], list[dict]]:
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    valid, invalid = [], []
    for idx, row in df.iterrows():
        raw = row.to_dict()
        try:
            raw["score"] = float(raw.get("score", 0))
        except ValueError:
            raw["_validation_error"] = f"Row {idx}: score is not numeric"
            invalid.append(raw)
            continue
        try:
            record = AssessmentRecord(**raw)
            valid.append(record.model_dump())
        except ValidationError as exc:
            raw["_validation_error"] = str(exc.errors())
            invalid.append(raw)
    return valid, invalid


# ── Phase 2: LLM Categorisation ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are an academic integrity officer at an online learning platform.
Review the assessment record and classify it into EXACTLY one of:
  - Satisfactory Performance
  - At-Risk Student: Intervene
  - Academic Integrity Flag

Respond with JSON only. Format:
{"category": "<label>", "reason": "<one sentence>"}"""


def llm_categorise(course: str, score: float, student_id: str) -> dict:
    user_msg = (
        f"Student ID: {student_id}\n"
        f"Course: {course}\n"
        f"Score: {score}/100\n"
        "Classify this assessment record."
    )
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
        )
        return json.loads(response["message"]["content"].strip())
    except json.JSONDecodeError:
        return {"category": "At-Risk Student: Intervene", "reason": "LLM returned non-JSON response."}
    except Exception as exc:
        return {"category": "At-Risk Student: Intervene", "reason": f"LLM error: {exc}"}


def run_llm_pass(records: list[dict]) -> list[dict]:
    print(f"[LLM]   Running {OLLAMA_MODEL} on {len(records)} rows...")
    enriched = []
    for rec in records:
        result = llm_categorise(rec["course_code"], rec["score"], rec["student_id"])
        rec["llm_category"] = result.get("category", "At-Risk Student: Intervene")
        rec["llm_reason"]   = result.get("reason", "")
        icon = {"Satisfactory Performance": "✅", "Academic Integrity Flag": "🚨", "At-Risk Student: Intervene": "⚠️"}.get(rec["llm_category"], "❓")
        print(f"  {icon}  {rec['student_id']:10s} | Score: {rec['score']:>6.1f} | {rec['llm_category']}")
        enriched.append(rec)
    return enriched


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not INPUT_CSV.exists():
        print(f"[ERROR] Input file not found: {INPUT_CSV}")
        sys.exit(1)

    print(f"\n{'═'*60}")
    print(f"  PHASE 1 — Deterministic Rules (Score Range + Code Validation)")
    print(f"{'═'*60}")
    print(f"[INFO]  Loading → {INPUT_CSV}")
    valid_rows, invalid_rows = load_and_validate(INPUT_CSV)
    print(f"[INFO]  Validated {len(valid_rows)} rows | Rejected {len(invalid_rows)} invalid rows")

    if invalid_rows:
        print("[WARN]  Violations:")
        for r in invalid_rows:
            print(f"         • {r.get('student_id', 'N/A')} — {r.get('_validation_error')}")

    at_risk = [r for r in valid_rows if r["score"] < LOW_SCORE_THRESHOLD]
    print(f"[INFO]  At-risk flag: {len(at_risk)} rows with score < {LOW_SCORE_THRESHOLD}")

    print(f"\n{'═'*60}")
    print(f"  PHASE 2 — Probabilistic Intelligence ({OLLAMA_MODEL})")
    print(f"{'═'*60}")
    enriched_rows = run_llm_pass(valid_rows)

    enriched_df = pd.DataFrame(enriched_rows)
    final_df    = enriched_df[enriched_df["score"] < LOW_SCORE_THRESHOLD].copy()
    final_df["rule_flag"] = final_df["score"].apply(
        lambda s: f"score {s:.1f} is below intervention threshold {LOW_SCORE_THRESHOLD:.1f}"
    )
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[INFO]  Saved → {OUTPUT_CSV}")

    print(f"\n{'═'*60}")
    print(f"  ASSESSMENT AUDIT SUMMARY")
    print(f"{'═'*60}")
    print(final_df[["student_id", "course_code", "score", "rule_flag", "llm_category", "llm_reason"]].to_string(index=False))


if __name__ == "__main__":
    main()
