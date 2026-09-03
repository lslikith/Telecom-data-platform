{{ config(
    materialized='table'
) }}

WITH bills AS (
    SELECT * FROM {{ ref('stg_billing') }}
),

payments AS (
    SELECT
        BILL_ID,
        PAYMENT_ID,
        PAYMENT_DATETIME,
        PAYMENT_DATE,
        AMOUNT AS PAID_AMOUNT,
        PAYMENT_METHOD,
        PAYMENT_GATEWAY,
        TRANSACTION_STATUS,
        IS_SUCCESSFUL
    FROM {{ ref('stg_payments') }}
)

SELECT
    MD5(b.BILL_ID) AS BILLING_KEY,
    b.BILL_ID,
    b.CUSTOMER_ID,
    MD5(b.CUSTOMER_ID) AS CUSTOMER_KEY,
    b.BILLING_PERIOD,
    b.BILL_DATE,
    b.DUE_DATE,
    b.BASE_AMOUNT,
    b.ADDITIONAL_CHARGES,
    b.DISCOUNT_AMOUNT,
    b.TAX_AMOUNT,
    b.TOTAL_AMOUNT,
    b.PAYMENT_STATUS,
    b.IS_PAID,

    p.PAYMENT_ID,
    p.PAYMENT_DATETIME,
    p.PAYMENT_DATE,
    COALESCE(p.PAID_AMOUNT, 0) AS PAID_AMOUNT,
    p.PAYMENT_METHOD,
    p.PAYMENT_GATEWAY,
    p.TRANSACTION_STATUS,
    COALESCE(p.IS_SUCCESSFUL, FALSE) AS IS_PAYMENT_SUCCESSFUL,

    -- Payment delay days calculation
    CASE 
        WHEN p.PAYMENT_DATE IS NOT NULL 
        THEN DATEDIFF(day, b.BILL_DATE, p.PAYMENT_DATE)
        ELSE NULL
    END AS DAYS_TO_PAY,

    -- Due date adherence flag
    CASE 
        WHEN p.PAYMENT_DATE IS NOT NULL AND p.PAYMENT_DATE <= b.DUE_DATE THEN TRUE
        WHEN p.PAYMENT_DATE IS NOT NULL AND p.PAYMENT_DATE > b.DUE_DATE THEN FALSE
        ELSE NULL
    END AS PAID_ON_TIME,

    b.LOAD_DATE

FROM bills b
LEFT JOIN payments p
    ON b.BILL_ID = p.BILL_ID
