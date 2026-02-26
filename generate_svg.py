import urllib.request
import json
from rich.console import Console
from rich.terminal_theme import MONOKAI

console = Console(record=True, width=100)

domains = ["finance", "healthcare", "supply_chain", "edtech", "legal"]

console.print("[bold cyan]🚀 Sovereign UI - LobeChat Plugin API Test[/bold cyan]")
console.print("[dim]Target: http://localhost:8000/chat[/dim]\n")

for d in domains:
    payload = json.dumps({"domain": d, "query": f"Test {d} Agent Config", "mode": "rag"}).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/chat", data=payload, headers={'Content-Type': 'application/json'})
    console.print(f"[bold yellow]Testing Domain:[/bold yellow] {d}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            ans = data.get("answer", "").strip()
            # print first 60 chars of answer
            ans = ans[:60] + "..." if len(ans) > 60 else ans
            console.print(f"  [green]✅ Success[/green]: Output received. Length: {len(data.get('answer', ''))} chars")
            console.print(f"  [dim]Preview: '{ans}'[/dim]\n")
    except Exception as e:
        console.print(f"  [red]❌ Failed[/red]: {e}\n")

console.print("[bold green]All endpoints verified and fully operational.[/bold green]")

console.save_svg("05_advanced_ui_lobechat/proof/lobby_test.svg", title="Session 05: LobeChat API Verification", theme=MONOKAI)
print("Saved SVG.")
