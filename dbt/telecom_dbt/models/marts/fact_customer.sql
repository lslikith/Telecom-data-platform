{{ config(
    materialized='table'
) }}

SELECT
    MD5(CUSTOMER_ID) AS CUSTOMER_KEY,

    CUSTOMER_ID,

    CONTRACT,

    TENURE,

    MONTHLY_CHARGES,

    TOTAL_CHARGES,

    CASE
        WHEN CHURN = 'Yes' THEN 1
        WHEN CHURN = 'No' THEN 0
        ELSE NULL
    END AS CHURN_FLAG,

    LOAD_DATE

FROM {{ ref('stg_customers') }}