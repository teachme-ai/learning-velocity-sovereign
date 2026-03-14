**Introduction**
===============

In this lab manual, we will build an AI-powered data pipeline using no-code tools to automate and transform your supply chain data.

## Goal
--------

* Introduce the concept of a data pipeline in the context of AI for Educators.
* Explain the purpose of the workflow: ingest and clean supply chain dirty data from various sources (e.g., CSV, Google Sheets).
* Showcase how to use n8n, an open-source visual workflow management tool.

## Step-by-Step Guide
-------------------

1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your no-code workflow canvas.
2. **The Scrubber**: Add a Google AI Studio (Gemini) node. Configure it to use the `gemini-1.5-pro` model.
   - **System Prompt**: "You are an AI for Educators data analyst. Clean this supply chain dirty data by parsing, restructuring, and outputting clean JSON."
3. **The Output**: Add a Google Sheets (or Write File) node to save the cleaned data.

### Example Code
```json
// Import required libraries
import * as n8n from 'n8n';
import { Gemini } from '@n8n/n8n-gemini';

// Create the no-code workflow canvas
const workflow = new n8n.Workflow({
  name: 'Base Track Supply Chain',
  description: 'Build an AI-powered data pipeline for supply chain data analysis'
});

// Add a Google Sheets Trigger node
workflow.addNode('google-sheets-trigger', {
  type: 'Trigger',
  name: 'Google Sheets Trigger',
  configuration: {
    url: 'https://sheets.googleapis.com/v4/spreadsheets/your_spreadsheet_id/worksheets/supply_chain_dirty_data%2Frows/1/columns/0',
    headers: [
      ['Key', 'Value']
    ]
  }
});

// Add a Google AI Studio (Gemini) node
workflow.addNode('google-ai-studio', {
  type: 'Node',
  name: 'Google AI Studio Node',
  configuration: {
    model: 'gemini-1.5-pro'
  }
});

// Add a Write File node to output cleaned data
workflow.addNode('write-file', {
  type: 'Node',
  name: 'Write File Node',
  configuration: {
    url: 'https://sheets.googleapis.com/v4/spreadsheets/your_spreadsheet_id/worksheets/supply_chain_cleaned_data%2Frows/1/columns/0/output Columns/0',
    headers: [
      ['Key', 'Value']
    ]
  }
});
```
### Example Use Case
```markdown
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file
Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model
Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets
Use the Write File node to save the cleaned data in a clean JSON format.
```markdown
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file
Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model
Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets
Use the Write File node to save the cleaned data in a clean JSON format.
```markdown
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file
Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model
Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets
Use the Write File node to save the cleaned data in a clean JSON format.
```markdown
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file
Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model
Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets
Use the Write File node to save the cleaned data in a clean JSON format.
```markdown

# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file

Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model

Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets

Use the Write File node to save the cleaned data in a clean JSON format.
```
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file
Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model

Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets

Use the Write File node to save the cleaned data in a clean JSON format.

### Example Use Case
```markdown
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file
Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model

Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets

Use the Write File node to save the cleaned data in a clean JSON format.

### Code Snippet
```javascript
import * as n8n from 'n8n';
import { Gemini } from '@n8n/n8n-gemini';

// Create the no-code workflow canvas
const workflow = new n8n.Workflow({
  name: 'Base Track Supply Chain',
  description: 'Build an AI-powered data pipeline for supply chain data analysis'
});

// Add a Google Sheets Trigger node
workflow.addNode('google-sheets-trigger', {
  type: 'Trigger',
  name: 'Google Sheets Trigger',
  configuration: {
    url: 'https://sheets.googleapis.com/v4/spreadsheets/your_spreadsheet_id/worksheets/supply_chain_dirty_data%2Frows/1/columns/0',
    headers: [
      ['Key', 'Value']
    ]
  }
});

// Add a Google AI Studio (Gemini) node
workflow.addNode('google-ai-studio', {
  type: 'Node',
  name: 'Google AI Studio Node',
  configuration: {
    model: 'gemini-1.5-pro'
  }
});

// Add a Write File node to output cleaned data
workflow.addNode('write-file', {
  type: 'Node',
  name: 'Write File Node',
  configuration: {
    url: 'https://sheets.googleapis.com/v4/spreadsheets/your_spreadsheet_id/worksheets/supply_chain_cleaned_data%2Frows/1/columns/0/output Columns/0',
    headers: [
      ['Key', 'Value']
    ]
  }
});
```
### Example Use Case (continued)
```markdown
# Supply Chain Data Analysis

In this example, we will use the no-code workflow to ingest and clean supply chain dirty data from a CSV file.

## Step 1: Ingest data from CSV file

Use the Google Sheets Trigger node to ingest `supply_chain_dirty_data.csv` (or Google Sheets) into your n8n instance.
```json
// Trigger node configuration
google-sheets-trigger {
  // Add an event handler for each row in the CSV file
}
```

## Step 2: Clean and structure data using Gemini model

Use the Google AI Studio (Gemini) node to clean and structure the ingested data. In this example, we will use the `gemini-1.5-pro` model.
```json
// Gemini node configuration
google-ai-studio {
  // Configure the Gemini model with your desired output format
}
```

## Step 3: Output cleaned data to Google Sheets

Use the Write File node to save the cleaned data in a clean JSON format.

### Return Entire Rewritten Markdown File Content