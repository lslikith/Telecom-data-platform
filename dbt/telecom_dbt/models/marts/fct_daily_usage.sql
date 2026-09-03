{{ config(
    materialized='table'
) }}

WITH usage AS (
    SELECT * FROM {{ ref('stg_usage') }}
),

towers AS (
    SELECT TOWER_ID, CITY, STATE, TECHNOLOGY FROM {{ ref('stg_towers') }}
)

SELECT
    MD5(u.USAGE_ID) AS USAGE_KEY,
    u.USAGE_ID,
    u.CUSTOMER_ID,
    MD5(u.CUSTOMER_ID) AS CUSTOMER_KEY,
    u.USAGE_DATE,
    u.TOWER_ID,
    MD5(u.TOWER_ID) AS TOWER_KEY,

    t.CITY AS TOWER_CITY,
    t.STATE AS TOWER_STATE,
    t.TECHNOLOGY AS NETWORK_TECH,

    u.VOICE_MINUTES,
    u.DATA_USAGE_MB,
    u.DATA_USAGE_GB,
    u.SMS_COUNT,
    u.IS_ROAMING,

    -- High data consumer flag (> 2GB / day)
    CASE WHEN u.DATA_USAGE_GB >= 2.0 THEN TRUE ELSE FALSE END AS IS_HEAVY_DATA_USER,

    u.LOAD_DATE

FROM usage u
LEFT JOIN towers t
    ON u.TOWER_ID = t.TOWER_ID
