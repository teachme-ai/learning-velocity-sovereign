# Sustainability & ESG (Set A) — Base Track: Data Pipeline (No-Code)

Welcome to the **Base Track** for Sustainability & ESG. Here we orchestrate the data cleaning pipeline using visual node-based workflows.

## Goal
Build an **n8n** workflow that ingests `sustainability_and_esg_dirty_data.csv` (or Google Sheets) and uses a **Google AI Studio (Gemini)** node to clean and structure it.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model.
   - **System Prompt**: "You are a Sustainability & ESG data analyst. Parse this messy row and output clean JSON."
3. **The Output**: Add a **Google Sheets (or Write File)** node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
# Limit context window

### Sustainability & ESG Industry Context
In today's fast-paced business environment, companies must balance sustainability and environmental responsibility with financial performance. Effective ESG management can lead to increased investor confidence, cost savings, and long-term competitive advantage.

## Business Value of the Workflow
The no-code **Base Track** for Sustainability & ESG provides a foundation for organizations to develop and deploy data-driven solutions that drive meaningful impact. By leveraging industry-standard tools like n8n and Google AI Studio, companies can:

* Enhance their sustainability analytics capabilities
* Improve financial modeling with ESG considerations
* Develop predictive models for risk management and mitigation

The resulting workflow will enable businesses to make more informed decisions, reduce costs, and optimize their ESG strategy.