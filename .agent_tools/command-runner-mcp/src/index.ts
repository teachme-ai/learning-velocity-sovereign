#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { spawn } from "child_process";
import { appendFileSync, mkdirSync } from "fs";
import { dirname } from "path";

const LOG_FILE = "/tmp/q_agent_log.txt";

function log(agentName: string, command: string, cwd: string, line: string, isHeader = false) {
  const ts = new Date().toTimeString().slice(0, 8);
  let entry: string;
  if (isHeader) {
    entry = [
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      `⏱  ${ts}  │  🤖 ${agentName}  │  📂 ${cwd}`,
      `▶  ${command}`,
      "────────────────────────────────────────────────────────",
    ].join("\n");
  } else {
    entry = line;
  }
  try {
    mkdirSync(dirname(LOG_FILE), { recursive: true });
    appendFileSync(LOG_FILE, entry + "\n");
  } catch {}
}

function runCommand(command: string, cwd: string, agentName: string): Promise<{ output: string; exitCode: number }> {
  return new Promise((resolve) => {
    log(agentName, command, cwd, "", true);

    const proc = spawn("bash", ["-c", command], { cwd, env: process.env });
    const lines: string[] = [];

    const onData = (data: Buffer) => {
      data.toString().split("\n").filter(Boolean).forEach((line) => {
        log(agentName, command, cwd, line);
        lines.push(line);
      });
    };

    proc.stdout.on("data", onData);
    proc.stderr.on("data", onData);

    proc.on("close", (code) => {
      const exitCode = code ?? 1;
      const footer = [
        "────────────────────────────────────────────────────────",
        exitCode === 0
          ? `✅ Exit: ${exitCode}  │  Completed at ${new Date().toTimeString().slice(0, 8)}`
          : `❌ Exit: ${exitCode}  │  Failed at ${new Date().toTimeString().slice(0, 8)}`,
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      ].join("\n");
      appendFileSync(LOG_FILE, footer + "\n");
      resolve({ output: lines.join("\n"), exitCode });
    });
  });
}

const server = new Server(
  { name: "command-runner-mcp", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "run_command",
      description:
        "Execute a shell command and stream output to the shared agent log at /tmp/q_agent_log.txt. All agents should use this tool for full cross-agent visibility.",
      inputSchema: {
        type: "object",
        properties: {
          command: { type: "string", description: "Shell command to execute" },
          cwd: { type: "string", description: "Working directory", default: "/tmp" },
          agent_name: { type: "string", description: "Name of the calling agent (e.g. 'Amazon Q', 'Gemini', 'Claude')", default: "unknown" },
        },
        required: ["command"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "run_command") {
    throw new Error(`Unknown tool: ${request.params.name}`);
  }

  const { command, cwd = process.cwd(), agent_name = "unknown" } = request.params.arguments as {
    command: string;
    cwd?: string;
    agent_name?: string;
  };

  const { output, exitCode } = await runCommand(command, cwd, agent_name);

  return {
    content: [
      {
        type: "text",
        text: output || "(no output)",
      },
    ],
    isError: exitCode !== 0,
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
