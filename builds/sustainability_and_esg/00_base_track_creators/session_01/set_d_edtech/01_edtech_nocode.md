# Introduction
Welcome to the Sustainability & ESG Industry Lab Manual: **Base Track** for EdTech. This guide will walk you through building a data pipeline using visual node-based workflows, leveraging no-code tools.

## Goal
Build an n8n workflow that ingests `edtech_dirty_data.csv` (or Google Sheets) and uses a Google AI Studio (Gemini) node to clean and structure it for ESG analysis in the Sustainability & ESG industry.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a Google AI Studio node. Configure it to use the `gemini-1.5-pro` model, selecting topics related to Sustainability & ESG, such as environmental impact analysis or social responsibility metrics.
   - **System Prompt**: "You are a sustainability consultant. Analyze data on renewable energy usage and output clean JSON."
3. **The Output**: Add a Google Sheets (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window

# Business Value
## EdTech's Role in Sustainability & ESG
EdTech plays a crucial role in supporting the transition to a sustainable and resilient future. By incorporating ESG considerations into their operations, companies can:
* Enhance their brand reputation and customer loyalty
* Improve their bottom line through cost savings and increased efficiency
* Contribute to reducing greenhouse gas emissions and mitigating climate change

## Industry Impact
The Sustainability & ESG industry is growing rapidly, driven by increasing consumer demand for environmentally friendly products and services. EdTech can capitalize on this trend by:
* Developing innovative solutions that address pressing environmental issues
* Collaborating with other companies to accelerate the transition to a sustainable future
* Providing data-driven insights and recommendations to inform business decisions

By focusing on sustainability and ESG, EdTech can differentiate itself from competitors, build trust with customers, and drive long-term success in this rapidly evolving industry.