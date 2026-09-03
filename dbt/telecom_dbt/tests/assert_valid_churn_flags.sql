-- Singular test: Verify that churn flag is strictly 0 or 1
SELECT
    CUSTOMER_ID,
    CHURN_FLAG
FROM {{ ref('dim_customers') }}
WHERE CHURN_FLAG NOT IN (0, 1)
   OR CHURN_FLAG IS NULL
