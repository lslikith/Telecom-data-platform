{% docs __overview__ %}

# Telecom Analytics Platform

Welcome to the **Telecom Data Platform** dbt documentation.

## Architecture & Data Flow

The platform processes telecom operational feeds through a medallion architecture on **Snowflake**:

1. **Bronze (RAW)**: Operational tables loaded from CRM, RAN cell towers, billing systems, usage records, customer care tickets, and network outage incident logs.
2. **Silver (STAGING)**: Standardized, deduplicated, and clean typed views. Null values, dates, and boolean flags are normalized.
3. **Gold (MARTS)**: Dimensional models (`dim_customers`, `dim_plans`, `dim_towers`), transactional fact tables (`fct_billing_payments`, `fct_daily_usage`, `fct_support_tickets`), SCD Type 2 history snapshots, and analytical marts (`churn_risk_analysis`, `churn_by_contract`, `network_performance_marts`).

## Key Performance Indicators (KPIs)

- **Churn Rate**: Percentage of subscribers leaving each month categorized by contract and payment method.
- **Churn Risk Tiering**: Predictive scoring based on tenure, service count, overdue payments, and customer care complaints.
- **Average Revenue Per User (ARPU)**: Tracked across contract cohorts and plan categories.
- **Cell Tower Availability**: Uptime and degradation tracking correlated with subscriber service quality.

{% enddocs %}
