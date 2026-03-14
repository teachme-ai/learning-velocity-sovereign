# Introduction
Welcome to the **Base Track** for AI for Global Finance Supply Chain. Here we orchestrate the data pipeline using visual node-based workflows tailored specifically for the finance industry.

## Goal
Build an n8n workflow that ingests `supply_chain_dirty_data.csv` (or Google Sheets) and uses a Google AI Studio (Gemini) node to clean and structure it, preparing it for further processing in the Supply Chain.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model, setting the system prompt to "You are an expert in Supply Chain data analysis. Intelligently clean this mess and output structured JSON."
3. **The Output**: Add a **Google Sheets** (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
# Business Value
### Key Benefits for Finance Industry Professionals

By implementing this workflow, finance professionals can:

1. **Improve Data Quality**: Automatically clean and preprocess messy supply chain data, reducing errors and increasing accuracy.
2. **Enhance Operational Efficiency**: Streamline data processing and analysis, enabling faster decision-making in real-time.
3. **Unlock Business Insights**: Gain actionable insights from cleaned data, informing strategic business decisions.
4. **Meet Regulatory Requirements**: Comply with industry regulations and standards by ensuring data is properly structured and cleaned.

### ROI Potential

* **Reduced Costs**: Decrease manual labor costs associated with data cleaning and preprocessing.
* **Increased Productivity**: Free up time for higher-value activities, such as analysis and strategic decision-making.
* **Improved Customer Experience**: Deliver accurate and timely information to customers, enhancing their overall experience.