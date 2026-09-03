{{ config(
    materialized='table'
) }}

WITH tickets AS (
    SELECT * FROM {{ ref('stg_support_tickets') }}
),

customers AS (
    SELECT CUSTOMER_ID, CHURN_FLAG, CONTRACT, TENURE_MONTHS FROM {{ ref('stg_customers') }}
)

SELECT
    MD5(t.TICKET_ID) AS TICKET_KEY,
    t.TICKET_ID,
    t.CUSTOMER_ID,
    MD5(t.CUSTOMER_ID) AS CUSTOMER_KEY,

    t.CATEGORY,
    t.PRIORITY,
    t.CHANNEL,
    t.CREATED_AT,
    t.RESOLVED_AT,
    t.RESOLUTION_TIME_HOURS,
    t.STATUS,
    t.IS_RESOLVED,
    t.SATISFACTION_SCORE,

    c.CONTRACT AS CUSTOMER_CONTRACT,
    c.TENURE_MONTHS AS CUSTOMER_TENURE,
    c.CHURN_FLAG,

    CASE 
        WHEN t.SATISFACTION_SCORE <= 2 THEN 'Detractor'
        WHEN t.SATISFACTION_SCORE = 3 THEN 'Passive'
        WHEN t.SATISFACTION_SCORE >= 4 THEN 'Promoter'
        ELSE 'Unrated'
    END AS CSAT_CATEGORY,

    t.LOAD_DATE

FROM tickets t
LEFT JOIN customers c
    ON t.CUSTOMER_ID = c.CUSTOMER_ID
