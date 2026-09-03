# Snowflake Infrastructure & Scripts Guide

This directory contains the complete Snowflake SQL infrastructure and analytical worksheets for the **Telecom Data Platform**.

## Scripts Overview

| File | Purpose | Layer |
| :--- | :--- | :--- |
| [`00_environment_setup.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/00_environment_setup.sql) | Creates `TELECOM_WH` warehouse, `TELECOM_DB` database, and `RAW`, `STAGING`, `MARTS` schemas | Infrastructure |
| [`01_file_formats.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/01_file_formats.sql) | Defines standard CSV file format with headers, quoting, and null handling | Ingestion |
| [`02_stages.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/02_stages.sql) | Creates internal `CRM_STAGE` for staging generated CSV files | Ingestion |
| [`03_raw_tables.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/03_raw_tables.sql) | Defines DDL for all 8 RAW tables (Customers, Plans, Towers, Billing, Payments, Usage, Support, Outages) | Schema / RAW |
| [`04_copy_into.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/04_copy_into.sql) | `COPY INTO` commands for loading staged CSV files into Snowflake RAW tables | Ingestion |
| [`05_validation.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/05_validation.sql) | Data quality and load audits, table row counts, primary key null checks | Quality Audit |
| [`06_queries.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/06_queries.sql) | High-impact business intelligence queries (Churn by Contract, ARPU, Outage Correlation, CSAT) | Analytics |
| [`07_storage_integrations.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/07_storage_integrations.sql) | Optional AWS S3 IAM Role storage integration for external stage | AWS Integration |
| [`08_external_stage.sql`](file:///Users/keerthana/projects/Telecom-data-platform/Telecom-data-platform/sql/08_external_stage.sql) | External S3 stage configuration pointing to S3 bucket | AWS Integration |

## Execution Sequence

In Snowflake Snowsight or Snowflake CLI:
1. Run `00_environment_setup.sql`
2. Run `01_file_formats.sql`
3. Run `02_stages.sql`
4. Run `03_raw_tables.sql`
5. Run `04_copy_into.sql` (after staging files via SnowSQL or Python loader)
6. Run `05_validation.sql`
7. Run `06_queries.sql`

Alternatively, execute the Python bootstrap script:
```bash
python src/telecom/bootstrap.py
```
This runs the entire end-to-end Snowflake setup, dataset generation, stage upload, and COPY INTO in a single command.
