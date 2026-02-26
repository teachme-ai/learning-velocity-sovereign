# Sustainability & ESG (Set B) — Base Track: Data Pipeline (No-Code)

Welcome to the **Base Track** for Sustainability & ESG. Here we orchestrate the data cleaning pipeline using visual node-based workflows.

## Goal
Build an n8n workflow that ingests `sustainability_and_esg_dirty_data.csv` (or Google Sheets) and uses a Google AI Studio (Gemini) node to clean and structure it.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a `Google AI Studio` node. Configure it to use the `gemini-1.5-pro` model, with the following inputs:
   - **System Prompt**: "You are a Sustainability & ESG data analyst. Parse this messy row and output clean JSON."
3. **The Output**: Add a Google Sheets (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window

## Introduction
In today's fast-paced business landscape, sustainability and environmental, social, and governance (ESG) factors are increasingly recognized as crucial components of a company's overall performance. As organizations strive to reduce their ecological footprint, improve stakeholder engagement, and enhance long-term value creation, the demand for robust ESG data analysis has skyrocketed.

To effectively address these demands, companies must have access to high-quality, structured data that can be easily integrated into decision-making processes. This is where the no-code workflow from n8n comes in – a powerful platform designed to simplify complex business operations and accelerate innovation.

### Business Value

#### Key Benefits
The ability to clean and structure ESG data using no-code workflows offers numerous benefits for companies, including:

* **Improved Decision-Making**: With accurate, reliable ESG data, organizations can make more informed decisions that align with their sustainability goals.
* **Enhanced Stakeholder Engagement**: By providing stakeholders with actionable insights, companies can foster deeper relationships and build trust in their brand.
* **Increased Valuation**: Well-maintained ESG data can significantly impact a company's valuation, as it contributes to a more complete understanding of its environmental and social footprint.

#### Competitive Advantage
By leveraging n8n's no-code workflow capabilities, organizations can:

* **Compete with Larger Players**: By having a robust, scalable platform for managing ESG data, companies can differentiate themselves from larger competitors.
* **Drive Innovation**: The ability to quickly prototype and test new workflows enables businesses to stay ahead of the curve in terms of innovation and adaptation.

#### Cost Savings
The no-code workflow offers significant cost savings by eliminating the need for expensive consultants or in-house development teams. This can be particularly beneficial for smaller organizations or startups looking to accelerate their ESG data management capabilities.

By adopting an n8n-based ESG data pipeline, companies can unlock a new level of efficiency and effectiveness, ultimately driving long-term value creation and competitiveness in today's fast-paced business environment.