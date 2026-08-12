-- =====================================================
-- STAGES
-- =====================================================

USE DATABASE TELECOM_DB;
USE SCHEMA RAW;

CREATE OR REPLACE STAGE CRM_STAGE
FILE_FORMAT = CSV_FILE_FORMAT;
