-- =====================================================
-- PROJECT : Telecom Analytics Platform
-- PURPOSE : Initial Snowflake Environment Setup
-- =====================================================

CREATE WAREHOUSE IF NOT EXISTS TELECOM_WH
WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

USE WAREHOUSE TELECOM_WH;

CREATE DATABASE IF NOT EXISTS TELECOM_DB;

USE DATABASE TELECOM_DB;

CREATE SCHEMA IF NOT EXISTS RAW;

CREATE SCHEMA IF NOT EXISTS STAGING;

CREATE SCHEMA IF NOT EXISTS MARTS;