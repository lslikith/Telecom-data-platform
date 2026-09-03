-- ==============================================================================
-- TELECOM DATA PLATFORM — SNOWFLAKE INFRASTRUCTURE SETUP
-- SCRIPT 02: File Formats, Internal Stages & External Storage Integrations
-- ==============================================================================

USE WAREHOUSE TELECOM_WH;
USE DATABASE TELECOM_DB;
USE SCHEMA RAW;

-- ------------------------------------------------------------------------------
-- 1. CSV FILE FORMAT DEFINITION
-- ------------------------------------------------------------------------------
CREATE OR REPLACE FILE FORMAT CSV_FILE_FORMAT
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', '', 'None', 'NaN')
    EMPTY_FIELD_AS_NULL = TRUE
    TRIM_SPACE = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    COMMENT = 'Standard CSV format for telecom operational datasets';

-- ------------------------------------------------------------------------------
-- 2. INTERNAL STAGE FOR DATASET INGESTION
-- ------------------------------------------------------------------------------
CREATE STAGE IF NOT EXISTS CRM_STAGE
    FILE_FORMAT = CSV_FILE_FORMAT
    COMMENT = 'Internal Snowflake stage for uploaded CRM, billing, usage, and tower CSVs';

-- ------------------------------------------------------------------------------
-- 3. OPTIONAL AWS S3 STORAGE INTEGRATION (FOR EXTERNAL STAGING)
-- ------------------------------------------------------------------------------
-- Uncomment to configure AWS S3 External Stage
/*
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE STORAGE INTEGRATION TELECOM_S3_INT
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = S3
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::155359185640:role/SnowflakeS3Role'
    STORAGE_ALLOWED_LOCATIONS = ('s3://telecom-data-platform-likith/raw/');

CREATE OR REPLACE STAGE TELECOM_S3_STAGE
    URL = 's3://telecom-data-platform-likith/raw/'
    STORAGE_INTEGRATION = TELECOM_S3_INT
    FILE_FORMAT = CSV_FILE_FORMAT;
*/

-- ------------------------------------------------------------------------------
-- 4. VERIFY STAGES & FORMATS
-- ------------------------------------------------------------------------------
SHOW FILE FORMATS IN SCHEMA TELECOM_DB.RAW;
SHOW STAGES IN SCHEMA TELECOM_DB.RAW;
LIST @CRM_STAGE;
