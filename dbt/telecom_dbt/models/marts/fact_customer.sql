{{ config(
    materialized='table'
) }}

SELECT
    MD5(CUSTOMER_ID) AS CUSTOMER_KEY,
    CUSTOMER_ID,
    CONTRACT,
    TENURE_MONTHS AS TENURE,
    MONTHLY_CHARGES,
    TOTAL_CHARGES,
    CHURN_FLAG,
    LOAD_DATE
FROM {{ ref('stg_customers') }}