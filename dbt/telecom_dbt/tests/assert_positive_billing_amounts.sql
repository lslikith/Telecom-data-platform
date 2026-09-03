-- Singular test: Verify that total billed amounts are always positive or zero
SELECT
    BILL_ID,
    TOTAL_AMOUNT
FROM {{ ref('fct_billing_payments') }}
WHERE TOTAL_AMOUNT < 0
