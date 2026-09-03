-- ==============================================================================
-- TELECOM DATA PLATFORM — SNOWFLAKE INFRASTRUCTURE SETUP
-- SCRIPT 01: Warehouse, Database, Schemas, Roles & Privileges
-- ==============================================================================

USE ROLE ACCOUNTADMIN;

-- ------------------------------------------------------------------------------
-- 1. VIRTUAL WAREHOUSE
-- ------------------------------------------------------------------------------
CREATE WAREHOUSE IF NOT EXISTS TELECOM_WH
WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 1
    SCALING_POLICY = 'STANDARD'
    COMMENT = 'Dedicated virtual warehouse for the Telecom Data Platform';

USE WAREHOUSE TELECOM_WH;

-- ------------------------------------------------------------------------------
-- 2. DATABASE
-- ------------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS TELECOM_DB
COMMENT = 'Central analytical database for telecom lakehouse and reporting';

USE DATABASE TELECOM_DB;

-- ------------------------------------------------------------------------------
-- 3. MEDALLION SCHEMAS
-- ------------------------------------------------------------------------------
-- Bronze Layer: Raw ingestion tables directly loaded from source feeds
CREATE SCHEMA IF NOT EXISTS TELECOM_DB.RAW
COMMENT = 'Bronze Layer: Raw ingested data from CRM, billing, usage, towers, and tickets';

-- Silver Layer: Standardized, deduplicated, and clean-typed views
CREATE SCHEMA IF NOT EXISTS TELECOM_DB.STAGING
COMMENT = 'Silver Layer: Standardized views with validated types and normalized flags';

-- Gold Layer: Dimensional models, fact tables, marts, and SCD2 snapshots
CREATE SCHEMA IF NOT EXISTS TELECOM_DB.MARTS
COMMENT = 'Gold Layer: Conformed dimensions, fact tables, KPIs, and churn risk marts';

-- ------------------------------------------------------------------------------
-- 4. VERIFICATION & SHOW OBJECTS
-- ------------------------------------------------------------------------------
SHOW WAREHOUSES LIKE 'TELECOM_WH';
SHOW SCHEMAS IN DATABASE TELECOM_DB;
