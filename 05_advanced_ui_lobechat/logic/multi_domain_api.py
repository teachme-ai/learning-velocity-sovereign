"""
Session 05 — Sovereign Cockpit: Multi-Domain API Bridge
========================================================
FastAPI router that acts as a single gateway to all 5 Genkit swarms (Session 03)
and RAG retrievers (Session 04) across Finance, Healthcare, Supply Chain, EdTech, Legal.

Run:
    /tmp/genkit_env/bin/pip install fastapi uvicorn httpx
    /tmp/genkit_env/bin/uvicorn logic.multi_domain_api:app --port 8000 --reload

LobeChat Plugin Endpoint:
    POST http://localhost:8000/chat
    Body: { "domain": "finance", "query": "What are the expense limits?" }
"""

import sys
import os
import asyncio
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── Add project root so we can import swarm and RAG modules ───────────────────
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

# ── Lazy imports of domain swarms + RAG flows ─────────────────────────────────
# Imported inside handlers to allow selective loading per domain

DOMAIN_CONFIG = {
    "finance": {
        "label": "Corporate Finance",
        "swarm_module": "03_multi_agent_systems.set_a_finance.logic.swarm",
        "swarm_flow": "finance_agent_swarm",
        "rag_module": "04_sovereign_knowledge_rag.set_a_finance.logic.ingest_and_query",
        "rag_flow": "finance_rag_flow",
        "swarm_input_field": "csv_data",
        "session01_output": "/tmp/finance_output/flagged_expenses.csv",
    },
    "healthcare": {
        "label": "Healthcare & HIPAA",
        "swarm_module": "03_multi_agent_systems.set_b_healthcare.logic.swarm",
        "swarm_flow": "healthcare_agent_swarm",
        "rag_module": "04_sovereign_knowledge_rag.set_b_healthcare.logic.ingest_and_query",
        "rag_flow": "healthcare_rag_flow",
        "swarm_input_field": "csv_data",
        "session01_output": "/tmp/healthcare_output/scrubbed_billing.csv",
    },
    "supply_chain": {
        "label": "Supply Chain & Logistics",
        "swarm_module": "03_multi_agent_systems.set_c_supply_chain.logic.swarm",
        "swarm_flow": "supply_chain_agent_swarm",
        "rag_module": "04_sovereign_knowledge_rag.set_c_supply_chain.logic.ingest_and_query",
        "rag_flow": "supply_chain_rag_flow",
        "swarm_input_field": "csv_data",
        "session01_output": "/tmp/supply_chain_output/scrubbed_inventory.csv",
    },
    "edtech": {
        "label": "EdTech & Academic Integrity",
        "swarm_module": "03_multi_agent_systems.set_d_edtech.logic.swarm",
        "swarm_flow": "edtech_agent_swarm",
        "rag_module": "04_sovereign_knowledge_rag.set_d_edtech.logic.ingest_and_query",
        "rag_flow": "edtech_rag_flow",
        "swarm_input_field": "csv_data",
        "session01_output": "/tmp/edtech_output/cleaned_logs.csv",
    },
    "legal": {
        "label": "Legal & M&A Due Diligence",
        "swarm_module": "03_multi_agent_systems.set_e_legal.logic.swarm",
        "swarm_flow": "legal_agent_swarm",
        "rag_module": "04_sovereign_knowledge_rag.set_e_legal.logic.ingest_and_query",
        "rag_flow": "legal_rag_flow",
        "swarm_input_field": "json_data",
        "session01_output": "/tmp/legal_output/scanned_clauses.json",
    },
}

# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="Sovereign Industry Agents — API Bridge",
    description=(
        "Routes chat queries to the appropriate Genkit Swarm (Multi-Agent, Session 03) "
        "and RAG Retriever (Sovereign Knowledge, Session 04) for each industry domain."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # LobeChat local plugin needs this
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Custom Trace Exporter for Session 06 ──────────────────────────────────────
import json
import contextvars
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
from opentelemetry.sdk.trace import ReadableSpan
from genkit.core.trace.default_exporter import extract_span_data
from genkit.core.tracing import add_custom_exporter

# Thread-safe context variable to track the active domain for this API request
ACTIVE_DOMAIN = contextvars.ContextVar("active_domain", default="unknown")

TRACE_DOMAIN_MAP = {}
TRACE_FILE_MAP = {}

class DomainTraceExporter(SpanExporter):
    def export(self, spans: list[ReadableSpan]) -> SpanExportResult:
        try:
            import datetime
            for span in spans:
                data = extract_span_data(span)
                trace_id = data["traceId"]
                
                # Derive domain from trace ID or span attributes
                domain = TRACE_DOMAIN_MAP.get(trace_id, "unknown")
                if domain == "unknown":
                    path_str = data.get("attributes", {}).get("genkit:path", "")
                    name_str = data.get("attributes", {}).get("genkit:name", "")
                    for d in ["finance", "healthcare", "supply_chain", "edtech", "legal"]:
                        if d in path_str or d in name_str:
                            domain = d
                            TRACE_DOMAIN_MAP[trace_id] = domain
                            break
                            
                out_dir = ROOT / "06_observability" / "audit_logs" / domain
                out_dir.mkdir(parents=True, exist_ok=True)
                
                if trace_id not in TRACE_FILE_MAP:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
                    TRACE_FILE_MAP[trace_id] = out_dir / f"trace_{timestamp}.json"
                elif domain != "unknown" and "unknown" in str(TRACE_FILE_MAP[trace_id]):
                    # Correct an earlier initialization to 'unknown' if we just learned the domain
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
                    old_path = TRACE_FILE_MAP[trace_id]
                    TRACE_FILE_MAP[trace_id] = out_dir / f"trace_{timestamp}.json"
                    if old_path.exists():
                        try:
                            # Move existing data to the correct location
                            import shutil
                            shutil.move(str(old_path), str(TRACE_FILE_MAP[trace_id]))
                        except Exception:
                            pass
                
                filepath = TRACE_FILE_MAP[trace_id]
                
                existing_data = {"traceId": trace_id, "spans": {}}
                if filepath.exists():
                    try:
                        with open(filepath, "r") as f:
                            existing_data = json.load(f)
                    except Exception:
                        pass
                
                existing_data["spans"].update(data["spans"])
                if not span.parent:
                    existing_data["displayName"] = data.get("displayName")
                    existing_data["startTime"] = data.get("startTime")
                    existing_data["endTime"] = data.get("endTime")
                    
                with open(filepath, "w") as f:
                    json.dump(existing_data, f, indent=2)
                    
        except Exception as e:
            print(f"Trace Export Error: {e}")
        return SpanExportResult.SUCCESS

# Register the global exporter
add_custom_exporter(DomainTraceExporter(), "domain_file_exporter")


# ── Request / Response schemas ────────────────────────────────────────────────
class ChatRequest(BaseModel):
    domain: str = Field(
        description="Industry domain: finance | healthcare | supply_chain | edtech | legal",
        examples=["finance"],
    )
    query: str = Field(
        description="The question to ask the Sovereign Agent for this domain",
        examples=["What is the maximum daily meal expense for domestic travel?"],
    )
    mode: str = Field(
        default="rag",
        description="'rag' for knowledge retrieval (default) or 'swarm' for multi-agent analysis",
    )


class ChatResponse(BaseModel):
    domain: str
    domain_label: str
    mode: str
    answer: str
    sources: list[str] = []


class HealthResponse(BaseModel):
    status: str
    domains: list[str]
    genkit_env: str
    ollama: str


# ── Helper: call RAG flow ─────────────────────────="──────────────────────────
async def run_rag(domain_key: str, query: str) -> tuple[str, list[str]]:
    """Load and run the RAG flow for the given domain."""
    import importlib

    cfg = DOMAIN_CONFIG[domain_key]
    # Normalise module path (replace hyphens/spaces, handle __init__)
    mod_path = cfg["rag_module"].replace("-", "_")

    # Dynamically import and run the ingest+query pipeline
    # Since these use ai.run_main(), we call the internal flow directly
    mod = importlib.import_module(mod_path)
    flow_fn = getattr(mod, cfg["rag_flow"])

    # RAGInput is defined in each module
    RAGInput = mod.RAGInput
    await mod.ingest()  # ensure ChromaDB is populated
    result = await flow_fn(RAGInput(query=query))
    return result.answer, []


# ── Helper: call Swarm flow ───────────────────────────────────────────────────
async def run_swarm(domain_key: str) -> str:
    """Load and run the swarm flow for the given domain, using Session 01 output."""
    import importlib

    cfg = DOMAIN_CONFIG[domain_key]
    data_path = cfg["session01_output"]

    if not os.path.exists(data_path):
        raise HTTPException(
            status_code=428,
            detail=f"Session 01 output not found at {data_path}. Run the data pipeline first.",
        )

    with open(data_path, "r") as f:
        raw_data = f.read()

    mod = importlib.import_module(cfg["swarm_module"].replace("-", "_"))
    flow_fn = getattr(mod, cfg["swarm_flow"])
    SwarmInput = mod.SwarmInput
    result = await flow_fn(SwarmInput(**{cfg["swarm_input_field"]: raw_data}))
    return result.report


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/", response_model=dict)
async def root():
    return {
        "service": "Sovereign Industry Agents — API Bridge",
        "version": "1.0.0",
        "domains": list(DOMAIN_CONFIG.keys()),
        "endpoints": {
            "chat": "POST /chat",
            "health": "GET /health",
            "domains": "GET /domains",
        },
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    import urllib.request

    # Check Ollama
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3):
            ollama_status = "✅ running"
    except Exception:
        ollama_status = "❌ unreachable"

    # Check venv
    genkit_env = "✅ ready" if os.path.exists("/tmp/genkit_env/bin/python3") else "❌ missing"

    return HealthResponse(
        status="ok",
        domains=list(DOMAIN_CONFIG.keys()),
        genkit_env=genkit_env,
        ollama=ollama_status,
    )


@app.get("/domains")
async def list_domains():
    return {
        k: {"label": v["label"], "modes": ["rag", "swarm"]}
        for k, v in DOMAIN_CONFIG.items()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    domain_key = req.domain.lower().replace(" ", "_").replace("-", "_")
    if domain_key not in DOMAIN_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown domain '{req.domain}'. Valid: {list(DOMAIN_CONFIG.keys())}",
        )

    # Set the ContextVar so the asynchronous trace exporter knows where to write
    token = ACTIVE_DOMAIN.set(domain_key)

    cfg = DOMAIN_CONFIG[domain_key]

    try:
        if req.mode == "swarm":
            answer = await run_swarm(domain_key)
            sources = ["Session 03 Multi-Agent Swarm"]
        else:
            answer, sources = await run_rag(domain_key, req.query)
            sources = ["Session 04 Sovereign RAG Knowledge Base"]

        return ChatResponse(
            domain=domain_key,
            domain_label=cfg["label"],
            mode=req.mode,
            answer=answer,
            sources=sources,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
    finally:
        ACTIVE_DOMAIN.reset(token)


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("logic.multi_domain_api:app", host="0.0.0.0", port=8000, reload=False)
