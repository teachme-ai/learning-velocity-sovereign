# AI for Global Finance (Set B) — Base Track: Multi-Agent Swarm (No-Code)

Welcome to the **Base Track** for AI for Global Finance. We will build a "Visual Swarm" using individual AI Agent nodes in n8n.

## Goal
Construct an n8n workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter**.

## Step-by-Step Guide

### 1. Trigger - The Input Node
Add an **Input** node to accept queries from a webhook trigger, which will be responsible for fetching data from various sources.
```json
[
  {
    "name": "Input",
    "type": "Trigger",
    "trigger": {
      "nodeType": "Webhook"
    }
  }
]
```

### 2. Analyst Node - The Data Processor
An AI Agent node, **Analyst**, will be responsible for analyzing the data received from the input node and generating a report.
```json
[
  {
    "name": "Analyst",
    "type": "Agent",
    "parameters": {
      "inputNode": ["Input"]
    }
  },
  {
    "name": "Report",
    "type": "Node",
    "outputNode": [
      {
        "name": "Report",
        "type": "Markdown"
      }
    ]
  }
]
```

### 3. Auditor Node - The Compliance Checker
An AI Agent node, **Auditor**, will verify the compliance of the data received from the analyst node and detect any potential issues.
```json
[
  {
    "name": "Auditor",
    "type": "Agent",
    "parameters": {
      "inputNode": ["Analyst"]
    }
  },
  {
    "name": "Check",
    "type": "Node",
    "outputNode": [
      {
        "name": "Result",
        "type": "Boolean"
      }
    ]
  }
]
```

### 4. Reporter Node - The Markdown Generator
An AI Agent node, **Reporter**, will synthesize the output of the auditor node into a markdown report.
```json
[
  {
    "name": "Reporter",
    "type": "Agent",
    "parameters": {
      "inputNode": ["Auditor"]
    }
  },
  {
    "name": "Report",
    "type": "Node",
    "outputNode": [
      {
        "name": "Report",
        "type": "Markdown"
      }
    ]
  }
]
```

### 5. Response - The Webhook Output
A webhook output node will be created to send the final report back to the user.
```json
[
  {
    "name": "Response",
    "type": "Node",
    "outputNode": [
      {
        "name": "Response",
        "type": "Webhook"
      }
    ]
  }
]
```

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window