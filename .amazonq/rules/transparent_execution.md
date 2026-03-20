# Agent Transparency Rule
# All bash commands MUST be executed through the transparent wrapper script
# so the user can see live output via `tail -f /tmp/q_agent_log.txt`

When executing any bash command, ALWAYS route it through the wrapper script:

```
bash "/Users/khalidirfan/projects/Ai Bootcamps/.agent_tools/run_visible.sh" "<command>" "<working_directory>"
```

- Never run bare commands directly via executeBash
- Always wrap the command string in quotes
- Always pass the working directory as the second argument
- The user monitors `/tmp/q_agent_log.txt` via a VS Code task or `tail -f` in a visible terminal
