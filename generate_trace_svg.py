import json
import glob
import os
from rich.console import Console
from rich.terminal_theme import MONOKAI
from rich.panel import Panel
from rich.tree import Tree

console = Console(record=True, width=110)

trace_dir = "06_observability/traces/healthcare"
files = glob.glob(os.path.join(trace_dir, "*.json"))
if not files:
    console.print("[red]No trace found![/red]")
else:
    latest = max(files, key=os.path.getmtime)
    with open(latest, "r") as f:
        data = json.load(f)
        
    console.print(f"[bold cyan]🔍 Genkit Trace Inspector — {data.get('traceId')}[/bold cyan]")
    
    tree = Tree(f"🛠️ [bold]healthcare_agent_swarm[/bold] (Total Time: {data.get('endTime', 0) - data.get('startTime', 0):.2f}ms)")
    
    for sid, sdata in data.get("spans", {}).items():
        name = sdata.get("displayName", "unknown")
        if "llama" in name:
            inp = sdata.get("attributes", {}).get("genkit:input", "").lower()
            if "analyst" in inp: role = "[blue]Clinical Analyst (Step 1)[/blue]"
            elif "auditor" in inp: role = "[yellow]Medical Auditor (Step 2)[/yellow]"
            elif "reporter" in inp: role = "[green]Compliance Reporter (Step 3)[/green]"
            else: role = "[dim]Unknown LLM Call[/dim]"
            
            latency = (sdata.get("endTime", 0) - sdata.get("startTime", 0)) / 1000000
            tree.add(f"{role} ⏱️ {latency:.2f}ms")

    console.print(Panel(tree, border_style="cyan"))

os.makedirs("assets/proof/session_06", exist_ok=True)
console.save_svg("assets/proof/session_06/healthcare_trace.svg", title="Session 06: Genkit Trace (Healthcare)", theme=MONOKAI)
print("Saved SVG.")
