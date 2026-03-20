# Shared Command Runner MCP — Wiring Guide

A single MCP server that gives every agent (Amazon Q, Gemini/Antigravity, Claude) a
unified audit trail at `/tmp/q_agent_log.txt`.

---

## Architecture

```
┌─────────────┐   run_command   ┌──────────────────────────┐
│  Amazon Q   │ ──────────────► │                          │
├─────────────┤                 │  command-runner-mcp      │──► /tmp/q_agent_log.txt
│   Gemini    │ ──────────────► │  (stdio MCP server)      │
├─────────────┤                 │  dist/index.js           │──► stdout (returned to agent)
│   Claude    │ ──────────────► │                          │
└─────────────┘                 └──────────────────────────┘
```

**Server location:** `.agent_tools/command-runner-mcp/dist/index.js`  
**Log file:** `/tmp/q_agent_log.txt`  
**Watch live:** `tail -f /tmp/q_agent_log.txt`

---

## Tool: `run_command`

| Parameter    | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| `command`   | string | ✅       | Shell command to execute                 |
| `cwd`       | string | —        | Working directory (default: process cwd) |
| `agent_name`| string | —        | Calling agent label in the log           |

---

## Wiring Status

| Agent              | Config File                                                                 | Status |
|--------------------|-----------------------------------------------------------------------------|--------|
| Amazon Q           | `~/.aws/amazonq/mcp.json`                                                   | ✅ Wired |
| Claude Desktop     | `~/Library/Application Support/Claude/claude_desktop_config.json`           | ✅ Wired |
| Claude Code CLI    | `~/.claude.json` (via `claude mcp add`)                                     | ✅ Wired |
| Antigravity/Gemini | `.mcp.json` (workspace root — auto-discovered)                              | ✅ Wired |

Amazon Q also has a rule in `.amazonq/rules/mcp_command_runner.md` that instructs it
to prefer `run_command` over its native `executeBash` tool.

---

## Log Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱  14:32:01  │  🤖 Gemini  │  📂 /project
▶  npm install
────────────────────────────────────────────────────────
... command output ...
────────────────────────────────────────────────────────
✅ Exit: 0  │  Completed at 14:32:45
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Fallback Behaviour

If the MCP server is unavailable (not registered, node missing, etc.) each agent
falls back gracefully:

- **Amazon Q** — falls back to native `executeBash` + `run_visible.sh` wrapper
  (rule in `.amazonq/rules/transparent_execution.md`)
- **Claude Code** — falls back to its built-in Bash tool
- **Gemini/Antigravity** — falls back to its built-in shell tool

The fallback for Amazon Q still writes to `/tmp/q_agent_log.txt` via `run_visible.sh`,
so the log remains populated even without the MCP server.

---

## Rebuild After Changes

```bash
cd ".agent_tools/command-runner-mcp"
npm run build
```

## Verify Server is Responding

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | node ".agent_tools/command-runner-mcp/dist/index.js"
```

Expected: JSON response containing `run_command` in the tools array.

## Clear the Log

```bash
> /tmp/q_agent_log.txt
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Amazon Q not using MCP | Server not loaded yet (requires IDE restart) | Restart VS Code / Amazon Q extension |
| Claude Desktop not picking up server | App needs restart after config change | Quit and reopen Claude Desktop |
| `node: command not found` in MCP spawn | PATH not inherited by agent process | Use absolute path: `$(which node)` in config |
| Log file not created | `/tmp` permissions issue | `touch /tmp/q_agent_log.txt && chmod 666 /tmp/q_agent_log.txt` |
| Antigravity not finding `.mcp.json` | Workspace root mismatch | Confirm Antigravity opened `/Users/khalidirfan/projects/Ai Bootcamps` as root |
