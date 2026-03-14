# Introduction
Welcome to the AI for Educators Industry Supply Chain Track: Base Track - Sovereign Cockpit (No-Code)

This project aims to build a web application that connects to an n8n swarm, enabling seamless data exchange between the user's input and the educational content provided. By utilizing React as the frontend framework, we will create a one-page dashboard for educators to track student progress.

## Goal
Design and develop a React-based single-page web app that integrates with our n8n swarm, allowing users to query and visualize their educational data in real-time.

## Step-by-Step Guide

### 1. Set up the project
Log into Lovable (or v0/Cursor) and create a new project.

### 2. Configure the React app
Create a new React component for the dashboard. Ensure it includes:
*   A text input field for user queries
*   A submit button to send the query to `http://localhost:5678/webhook/swarm`
*   A markdown-rendered response area

```jsx
import React, { useState } from 'react';

const Dashboard = () => {
  const [query, setQuery] = useState('');
  const [response, SetResponse] = useState('');

  const handleQuerySubmit = (e) => {
    e.preventDefault();
    fetch('http://localhost:5678/webhook/swarm', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    })
      .then((res) => res.json())
      .then((data) => SetResponse(data));
  };

  return (
    <div>
      <form onSubmit={handleQuerySubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter query..."
        />
        <button type="submit">Send Query</button>
      </form>
      <textarea
        value={response}
        onChange={(e) => SetResponse(e.target.value)}
        rows="30"
        cols="60"
        style={{ padding: 10, border: '1px solid #ccc', borderRadius: 5 }}
      />
    </div>
  );
};

export default Dashboard;
```

### 3. Link to n8n swarm
Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on `http://localhost:5678/webhook/swarm`.

```json
{
  "name": "Base Track - Sovereign Cockpit (No-Code)",
  "version": "1.0",
  "metadataVersion": "2.0",
  "description": "Sovereign Cockpit (No-Code) for Supply Chain",
  "outputFormat": "json"
}
```

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window