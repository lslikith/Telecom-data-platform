-- ==============================================================================
-- TELECOM DATA PLATFORM — SNOWFLAKE INFRASTRUCTURE SETUP
-- SCRIPT 07: SNAPSHOTS Layer (SCD Type 2 Historical Change Tracking)
-- ==============================================================================

USE WAREHOUSE TELECOM_WH;
USE DATABASE TELECOM_DB;
USE SCHEMA MARTS;

-- ------------------------------------------------------------------------------
-- 1. INSPECT SCD TYPE 2 SNAPSHOT TABLE
-- ------------------------------------------------------------------------------
-- The SNAP_CUSTOMERS snapshot maintains historical state records using
-- dbt's check strategy on CONTRACT, PAYMENT_METHOD, MONTHLY_CHARGES, and CHURN.
SELECT 
    DBT_SCD_ID,
    CUSTOMER_ID,
    CONTRACT,
    PAYMENT_METHOD,
    MONTHLY_CHARGES,
    CHURN,
    DBT_VALID_FROM,
    DBT_VALID_TO,
    DBT_UPDATED_AT
FROM TELECOM_DB.MARTS.SNAP_CUSTOMERS
LIMIT 10;

-- ------------------------------------------------------------------------------
-- 2. QUERYING ACTIVE VS HISTORICAL SNAPSHOT RECORDS
-- ------------------------------------------------------------------------------
-- Current active snapshot records (dbt_valid_to IS NULL)
SELECT 
    COUNT(*) AS CURRENT_ACTIVE_RECORDS
FROM TELECOM_DB.MARTS.SNAP_CUSTOMERS
WHERE DBT_VALID_TO IS NULL;

-- Historical expired records (records that have undergone state changes)
SELECT 
    COUNT(*) AS HISTORICAL_EXPIRED_RECORDS
FROM TELECOM_DB.MARTS.SNAP_CUSTOMERS
WHERE DBT_VALID_TO IS NOT NULL;

-- ------------------------------------------------------------------------------
-- 3. POINT-IN-TIME SUBSCRIBER CHURN RECONSTRUCTION
-- ------------------------------------------------------------------------------
-- Reconstruct customer churn status as of a specific historical timestamp:
SELECT 
    CUSTOMER_ID,
    CONTRACT,
    PAYMENT_METHOD,
    CHURN,
    DBT_VALID_FROM,
    DBT_VALID_TO
FROM TELECOM_DB.MARTS.SNAP_CUSTOMERS
WHERE DBT_VALID_FROM <= CURRENT_TIMESTAMP()
  AND (DBT_VALID_TO IS NULL OR DBT_VALID_TO > CURRENT_TIMESTAMP())
LIMIT 20;
