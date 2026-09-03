{% snapshot snap_customers %}

{{
    config(
        target_database='TELECOM_DB',
        target_schema='MARTS',
        unique_key='CUSTOMER_ID',
        strategy='check',
        check_cols=['CONTRACT', 'PAYMENT_METHOD', 'MONTHLY_CHARGES', 'CHURN'],
        invalidate_hard_deletes=True,
    )
}}

SELECT
    CUSTOMER_ID,
    GENDER,
    CONTRACT,
    PAYMENT_METHOD,
    MONTHLY_CHARGES,
    CHURN,
    LOAD_DATE
FROM {{ source('raw', 'raw_customers') }}

{% endsnapshot %}
