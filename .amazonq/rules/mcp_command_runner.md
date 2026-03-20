# Shared Command Runner MCP Rule

When executing shell commands, PREFER the `run_command` MCP tool over the native `executeBash` tool.

This ensures all agent activity — regardless of which agent (Amazon Q, Gemini, Claude) is running — 
is written to the shared audit log at `/tmp/q_agent_log.txt`.

## Tool usage

Always call `run_command` with:
- `command`: the shell command string
- `cwd`: the working directory (absolute path)
- `agent_name`: `"Amazon Q"`

## Fallback

Only use `executeBash` directly when the MCP server is unavailable or for read-only introspection 
(e.g. `listDirectory`, `fsRead`) that doesn't need audit logging.
