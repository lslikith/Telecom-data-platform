{{ config(
    materialized='table'
) }}

SELECT
    MD5(PLAN_ID) AS PLAN_KEY,
    PLAN_ID,
    PLAN_NAME,
    MONTHLY_PRICE,
    DATA_LIMIT_GB,
    IS_UNLIMITED_DATA,
    NETWORK_TYPE,
    VOICE_MINUTES,
    IS_UNLIMITED_VOICE,
    SMS_LIMIT,
    VALIDITY_DAYS,
    PLAN_CATEGORY,
    LOAD_DATE
FROM {{ ref('stg_plans') }}
