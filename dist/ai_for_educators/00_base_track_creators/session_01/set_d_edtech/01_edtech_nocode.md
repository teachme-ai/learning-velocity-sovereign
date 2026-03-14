## Introduction

Welcome to the **Base Track** for EdTech, specifically designed for AI-driven educational tools. In this track, you will learn how to create an intelligent data pipeline that integrates with Google Sheets and uses machine learning models like n8n to cleanse and structure your data.

## Business Value

By implementing this workflow in your EdTech application, you can:

* **Streamline Data Management**: Automate the cleaning process for large datasets, reducing manual effort and increasing productivity.
* **Improve Data Quality**: Use Google AI Studio's natural language processing capabilities to parse and format messy data into a structured format.
* **Enhance Business Insights**: Extract valuable information from cleaned data that can inform educational decisions or optimize learning outcomes.
* **Support Teacher Training**: Use the output of this pipeline to provide educators with actionable insights, enabling them to create more effective lesson plans.
* **Foster Data-Driven Decision Making**: Leverage machine learning models to identify patterns and trends in student data, informing curriculum development and resource allocation.

This workflow is designed to be flexible and adaptable to your specific EdTech application. By following the step-by-step guide outlined below, you can create a robust data pipeline that drives business value for your organization.

## Step-by-Step Guide

1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a `Gemini` AI Studio node and configure it to use the `gemini-1.5-pro` model for data cleaning.
   - **System Prompt**: "You are an EdTech data analyst. Parse this messy row and output clean JSON."
3. **The Output**: Add a Google Sheets (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window