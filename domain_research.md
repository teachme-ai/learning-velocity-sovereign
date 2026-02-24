# Multi-Domain Authority: Initial Domain Research

This document outlines the sample schemas and data cleaning rules for **Set B: Healthcare** and **Set C: Supply Chain**, derived using the Deep Researcher capability.

---

## 🏥 Set B: Healthcare (Patient Data & Billing)

**Domain Context**: Validating hospital admission records and treatment billing for compliance and accuracy.

### Sample CSV Schema
| Column Name        | Data Type | Description                              |
| :---               | :---      | :---                                     |
| `patient_id`       | String    | Unique alphanumeric identifier (e.g., P-10023). |
| `admission_date`   | Date      | Date the patient was admitted (YYYY-MM-DD).|
| `diagnosis_code`   | String    | Standard ICD-10 format code (e.g., J01.90). |
| `treatment_cost`   | Float     | Total cost of the procedure/treatment in USD.|
| `insurance_provider`| String | Name of the insurance company.           |

### 3 Deterministic Cleaning Rules
1. **Cost Validity**: `treatment_cost` must be strictly greater than `$0.00` (No negative billing or zero-dollar entries without explicit flag).
2. **Temporal Logic**: `admission_date` cannot be in the future (relative to the system's current execution date).
3. **Format Compliance Check**: `diagnosis_code` must conform to standard ICD-10 structural formatting (e.g., 1 Letter followed by 2 digits, optionally followed by a dot and more digits).

---

## 🏭 Set C: Supply Chain (Inventory Management)

**Domain Context**: Auditing warehouse stock levels, pricing anomalies, and distribution logistics.

### Sample CSV Schema
| Column Name        | Data Type | Description                              |
| :---               | :---      | :---                                     |
| `item_sku`         | String    | Standard Stock Keeping Unit (e.g., WH-9942).    |
| `warehouse_id`     | String    | Identifier for the physical location.    |
| `stock_quantity`   | Integer   | Current number of units in the warehouse.|
| `unit_price`       | Float     | Price per single unit in USD.            |
| `last_restock_date`| Date      | Date the item was last added to inventory.|

### 3 Deterministic Cleaning Rules
1. **Physical Reality Check**: `stock_quantity` must be greater than or equal to `0` (Negative physical stock is impossible).
2. **Pricing Integrity**: `unit_price` must be strictly greater than `$0.00`. High-value thresholds (e.g., `> $5,000`) should trigger human/LLM review.
3. **SKU Standardization**: `item_sku` must follow the strict corporate alphanumeric pattern to prevent ghost inventory (e.g., Prefix-Numbers).
