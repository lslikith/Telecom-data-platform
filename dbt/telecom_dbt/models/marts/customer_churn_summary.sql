{{ config(
    materialized='table'
) }}

SELECT
    COUNT(*) AS TOTAL_CUSTOMERS,

    SUM(CHURN_FLAG) AS CHURNED_CUSTOMERS,

    COUNT(*) - SUM(CHURN_FLAG) AS ACTIVE_CUSTOMERS,

    ROUND(
        SUM(CHURN_FLAG) * 100.0 / COUNT(*),
        2
    ) AS CHURN_RATE_PERCENT

FROM {{ ref('fact_customer') }}