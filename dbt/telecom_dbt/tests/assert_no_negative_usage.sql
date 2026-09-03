-- Singular test: Verify that cellular data and voice minutes usage are non-negative
SELECT
    USAGE_ID,
    VOICE_MINUTES,
    DATA_USAGE_GB
FROM {{ ref('fct_daily_usage') }}
WHERE VOICE_MINUTES < 0
   OR DATA_USAGE_GB < 0
