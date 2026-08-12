-- =====================================================
-- FILE FORMATS
-- =====================================================

USE DATABASE TELECOM_DB;

CREATE OR REPLACE FILE FORMAT CSV_FILE_FORMAT
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
NULL_IF = ('NULL', '')
EMPTY_FIELD_AS_NULL = TRUE;