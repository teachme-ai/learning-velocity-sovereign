# Introduction
Welcome to the **Base Track** for Legal, a foundational module designed specifically for educators who want to integrate AI into their legal practice.

## Goal
Construct an n8n workflow that enables three parallel or sequential AI Agent nodes: 
- An Analyst node that analyzes legal trends.
- A Reporter node that synthesizes the output and generates a markdown report.
- An Auditor node that verifies compliance with regulatory requirements.

## Step-by-Step Guide

1. **The Trigger**: Add a Webhook Trigger node to receive user queries.
2. **The Analyst Node**: An AI Agent node prompting an Analyst node to analyze legal trends.
3. **The Auditor Node**: An AI Agent node prompted by the Analyst to verify compliance and catch hallucinations.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report based on the results from both the Analyst and Auditor nodes.
5. **The Response**: Send a Webhook Response back to the user.

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window

# Business Value
This AI for Educators module offers several business benefits:
- **Increased Efficiency**: Automate routine tasks, freeing up time for more strategic and high-value activities.
- **Improved Accuracy**: Reduce errors caused by manual data entry or analysis, resulting in higher accuracy rates.
- **Enhanced Customer Experience**: Personalize responses based on individual needs and preferences using machine learning algorithms.
- **Competitive Advantage**: Differentiate your legal practice with cutting-edge technology and expert analysis.