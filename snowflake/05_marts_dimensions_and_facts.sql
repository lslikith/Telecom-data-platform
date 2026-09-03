-- ==============================================================================
-- TELECOM DATA PLATFORM — SNOWFLAKE INFRASTRUCTURE SETUP
-- SCRIPT 05: MARTS Layer Dimensions & Fact Tables (Gold Layer)
-- ==============================================================================

USE WAREHOUSE TELECOM_WH;
USE DATABASE TELECOM_DB;
USE SCHEMA MARTS;

-- ------------------------------------------------------------------------------
-- 1. DIM_CUSTOMERS (Conformed Customer Dimension)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE DIM_CUSTOMERS AS
WITH ticket_summary AS (
    SELECT
        CUSTOMER_ID,
        COUNT(TICKET_ID) AS TOTAL_SUPPORT_TICKETS,
        AVG(SATISFACTION_SCORE) AS AVG_CSAT_SCORE
    FROM TELECOM_DB.STAGING.STG_SUPPORT_TICKETS
    GROUP BY CUSTOMER_ID
)
SELECT
    MD5(c.CUSTOMER_ID) AS CUSTOMER_KEY,
    c.CUSTOMER_ID,
    c.GENDER,
    c.SENIOR_CITIZEN,
    c.HAS_PARTNER,
    c.HAS_DEPENDENTS,
    c.TENURE_MONTHS,
    CASE
        WHEN c.TENURE_MONTHS = 0 THEN '00. New Subscriber'
        WHEN c.TENURE_MONTHS <= 12 THEN '01. 0 - 1 Year'
        WHEN c.TENURE_MONTHS <= 24 THEN '02. 1 - 2 Years'
        WHEN c.TENURE_MONTHS <= 48 THEN '03. 2 - 4 Years'
        ELSE '04. 4+ Years'
    END AS TENURE_COHORT,
    c.HAS_PHONE_SERVICE,
    c.MULTIPLE_LINES,
    c.INTERNET_SERVICE,
    c.ONLINE_SECURITY,
    c.ONLINE_BACKUP,
    c.DEVICE_PROTECTION,
    c.TECH_SUPPORT,
    c.STREAMING_TV,
    c.STREAMING_MOVIES,
    (
        CASE WHEN c.ONLINE_SECURITY = 'Yes' THEN 1 ELSE 0 END +
        CASE WHEN c.ONLINE_BACKUP = 'Yes' THEN 1 ELSE 0 END +
        CASE WHEN c.DEVICE_PROTECTION = 'Yes' THEN 1 ELSE 0 END +
        CASE WHEN c.TECH_SUPPORT = 'Yes' THEN 1 ELSE 0 END +
        CASE WHEN c.STREAMING_TV = 'Yes' THEN 1 ELSE 0 END +
        CASE WHEN c.STREAMING_MOVIES = 'Yes' THEN 1 ELSE 0 END
    ) AS ACTIVE_SERVICES_COUNT,
    c.CONTRACT,
    c.HAS_PAPERLESS_BILLING,
    c.PAYMENT_METHOD,
    c.MONTHLY_CHARGES,
    c.TOTAL_CHARGES,
    c.CHURN,
    c.CHURN_FLAG,
    CASE WHEN c.CHURN_FLAG = 1 THEN TRUE ELSE FALSE END AS IS_CHURNED,
    COALESCE(t.TOTAL_SUPPORT_TICKETS, 0) AS TOTAL_SUPPORT_TICKETS,
    ROUND(t.AVG_CSAT_SCORE, 2) AS AVG_CSAT_SCORE,
    c.LOAD_DATE
FROM TELECOM_DB.STAGING.STG_CUSTOMERS c
LEFT JOIN ticket_summary t
    ON c.CUSTOMER_ID = t.CUSTOMER_ID;

-- ------------------------------------------------------------------------------
-- 2. DIM_PLANS (Service Plans Dimension)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE DIM_PLANS AS
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
FROM TELECOM_DB.STAGING.STG_PLANS;

-- ------------------------------------------------------------------------------
-- 3. DIM_TOWERS (Network Cell Tower Dimension with Availability %)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE DIM_TOWERS AS
WITH outages_agg AS (
    SELECT
        TOWER_ID,
        COUNT(OUTAGE_ID) AS LIFETIME_OUTAGES_COUNT,
        SUM(DURATION_MINUTES) AS TOTAL_DOWNTIME_MINUTES,
        SUM(ESTIMATED_IMPACTED_USERS) AS TOTAL_SUBSCRIBERS_IMPACTED
    FROM TELECOM_DB.STAGING.STG_NETWORK_OUTAGES
    GROUP BY TOWER_ID
)
SELECT
    MD5(t.TOWER_ID) AS TOWER_KEY,
    t.TOWER_ID,
    t.TOWER_NAME,
    t.CITY,
    t.STATE,
    t.LATITUDE,
    t.LONGITUDE,
    t.TECHNOLOGY,
    t.VENDOR,
    t.CAPACITY,
    t.INSTALLATION_DATE,
    t.STATUS,
    t.IS_ACTIVE,
    COALESCE(o.LIFETIME_OUTAGES_COUNT, 0) AS LIFETIME_OUTAGES_COUNT,
    COALESCE(o.TOTAL_DOWNTIME_MINUTES, 0) AS TOTAL_DOWNTIME_MINUTES,
    COALESCE(o.TOTAL_SUBSCRIBERS_IMPACTED, 0) AS TOTAL_SUBSCRIBERS_IMPACTED,
    ROUND(
        100.0 - (COALESCE(o.TOTAL_DOWNTIME_MINUTES, 0) * 100.0 / (365 * 24 * 60)),
        3
    ) AS UPTIME_AVAILABILITY_PCT,
    t.LOAD_DATE
FROM TELECOM_DB.STAGING.STG_TOWERS t
LEFT JOIN outages_agg o
    ON t.TOWER_ID = o.TOWER_ID;

-- ------------------------------------------------------------------------------
-- 4. FCT_BILLING_PAYMENTS (Billing Fulfillment & Delinquency Fact)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE FCT_BILLING_PAYMENTS AS
WITH payments AS (
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
    FROM TELECOM_DB.STAGING.STG_PAYMENTS
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
    CASE 
        WHEN p.PAYMENT_DATE IS NOT NULL THEN DATEDIFF(day, b.BILL_DATE, p.PAYMENT_DATE)
        ELSE NULL
    END AS DAYS_TO_PAY,
    CASE 
        WHEN p.PAYMENT_DATE IS NOT NULL AND p.PAYMENT_DATE <= b.DUE_DATE THEN TRUE
        WHEN p.PAYMENT_DATE IS NOT NULL AND p.PAYMENT_DATE > b.DUE_DATE THEN FALSE
        ELSE NULL
    END AS PAID_ON_TIME,
    b.LOAD_DATE
FROM TELECOM_DB.STAGING.STG_BILLING b
LEFT JOIN payments p
    ON b.BILL_ID = p.BILL_ID;

-- ------------------------------------------------------------------------------
-- 5. FCT_DAILY_USAGE (Granular Daily Cellular Consumption Fact)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE FCT_DAILY_USAGE AS
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
    CASE WHEN u.DATA_USAGE_GB >= 2.0 THEN TRUE ELSE FALSE END AS IS_HEAVY_DATA_USER,
    u.LOAD_DATE
FROM TELECOM_DB.STAGING.STG_USAGE u
LEFT JOIN TELECOM_DB.STAGING.STG_TOWERS t
    ON u.TOWER_ID = t.TOWER_ID;

-- ------------------------------------------------------------------------------
-- 6. FCT_SUPPORT_TICKETS (Customer Care Complaints & Turnaround Fact)
-- ------------------------------------------------------------------------------
CREATE OR REPLACE TABLE FCT_SUPPORT_TICKETS AS
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
FROM TELECOM_DB.STAGING.STG_SUPPORT_TICKETS t
LEFT JOIN TELECOM_DB.STAGING.STG_CUSTOMERS c
    ON t.CUSTOMER_ID = c.CUSTOMER_ID;
