import os
import sys
import time
from pathlib import Path
import snowflake.connector

from telecom.config import (
    BILLING_DIR,
    CRM_SOURCE_FILE,
    OUTAGES_DIR,
    PAYMENTS_DIR,
    PLANS_DIR,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_ROLE,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_USER,
    SNOWFLAKE_WAREHOUSE,
    SUPPORT_DIR,
    TOWERS_DIR,
    USAGE_DIR,
)
from telecom.generators.run_daily import run_all_generators


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )


def bootstrap_snowflake():
    print("=" * 70)
    print("STARTING TELECOM DATA PLATFORM BOOTSTRAP")
    print("=" * 70)

    # 1. Run Data Generators
    print("\n[Step 1/5] Ensuring all synthetic datasets are generated...")
    run_all_generators()

    # 2. Connect to Snowflake
    print("\n[Step 2/5] Connecting to Snowflake...")
    conn = get_snowflake_connection()
    cur = conn.cursor()
    print(" Snowflake Connected Successfully!")

    # 3. Environment & Schema Setup
    print("\n[Step 3/5] Setting up Warehouse, Database, Schemas, File Format, and Stage...")
    setup_queries = [
        f"CREATE WAREHOUSE IF NOT EXISTS {SNOWFLAKE_WAREHOUSE} WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;",
        f"USE WAREHOUSE {SNOWFLAKE_WAREHOUSE};",
        f"CREATE DATABASE IF NOT EXISTS {SNOWFLAKE_DATABASE};",
        f"USE DATABASE {SNOWFLAKE_DATABASE};",
        "CREATE SCHEMA IF NOT EXISTS RAW;",
        "CREATE SCHEMA IF NOT EXISTS STAGING;",
        "CREATE SCHEMA IF NOT EXISTS MARTS;",
        "USE SCHEMA RAW;",
        """
        CREATE OR REPLACE FILE FORMAT CSV_FILE_FORMAT
        TYPE = CSV
        FIELD_DELIMITER = ','
        SKIP_HEADER = 1
        FIELD_OPTIONALLY_ENCLOSED_BY = '"'
        NULL_IF = ('NULL', '', 'None')
        EMPTY_FIELD_AS_NULL = TRUE;
        """,
        "CREATE STAGE IF NOT EXISTS CRM_STAGE FILE_FORMAT = CSV_FILE_FORMAT;",
    ]
    for q in setup_queries:
        cur.execute(q)

    # 4. Create RAW Tables
    print("\n[Step 4/5] Creating RAW tables in TELECOM_DB.RAW...")
    table_ddls = {
        "RAW_CUSTOMERS": """
            CREATE TABLE IF NOT EXISTS RAW_CUSTOMERS (
                CUSTOMER_ID STRING, GENDER STRING, SENIOR_CITIZEN NUMBER(1,0),
                PARTNER STRING, DEPENDENTS STRING, TENURE NUMBER(5,0),
                PHONE_SERVICE STRING, MULTIPLE_LINES STRING, INTERNET_SERVICE STRING,
                ONLINE_SECURITY STRING, ONLINE_BACKUP STRING, DEVICE_PROTECTION STRING,
                TECH_SUPPORT STRING, STREAMING_TV STRING, STREAMING_MOVIES STRING,
                CONTRACT STRING, PAPERLESS_BILLING STRING, PAYMENT_METHOD STRING,
                MONTHLY_CHARGES NUMBER(10,2), TOTAL_CHARGES STRING, CHURN STRING,
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_PLANS": """
            CREATE TABLE IF NOT EXISTS RAW_PLANS (
                PLAN_ID STRING, PLAN_NAME STRING, MONTHLY_PRICE NUMBER(10,2),
                DATA_LIMIT_GB NUMBER(10,0), NETWORK_TYPE STRING, VOICE_MINUTES NUMBER(10,0),
                SMS_LIMIT NUMBER(10,0), VALIDITY_DAYS NUMBER(5,0), PLAN_CATEGORY STRING,
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_TOWERS": """
            CREATE TABLE IF NOT EXISTS RAW_TOWERS (
                TOWER_ID STRING, TOWER_NAME STRING, CITY STRING, STATE STRING,
                LATITUDE NUMBER(10,6), LONGITUDE NUMBER(10,6), TECHNOLOGY STRING,
                VENDOR STRING, CAPACITY NUMBER(10,0), INSTALLATION_DATE DATE, STATUS STRING,
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_BILLING": """
            CREATE TABLE IF NOT EXISTS RAW_BILLING (
                BILL_ID STRING, CUSTOMER_ID STRING, BILLING_PERIOD STRING,
                BILL_DATE DATE, DUE_DATE DATE, BASE_AMOUNT NUMBER(10,2),
                ADDITIONAL_CHARGES NUMBER(10,2), DISCOUNT_AMOUNT NUMBER(10,2),
                TAX_AMOUNT NUMBER(10,2), TOTAL_AMOUNT NUMBER(10,2), PAYMENT_STATUS STRING,
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_PAYMENTS": """
            CREATE TABLE IF NOT EXISTS RAW_PAYMENTS (
                PAYMENT_ID STRING, BILL_ID STRING, CUSTOMER_ID STRING,
                PAYMENT_DATETIME TIMESTAMP_NTZ, AMOUNT NUMBER(10,2), PAYMENT_METHOD STRING,
                PAYMENT_GATEWAY STRING, TRANSACTION_STATUS STRING, TRANSACTION_REF STRING,
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_USAGE": """
            CREATE TABLE IF NOT EXISTS RAW_USAGE (
                USAGE_ID STRING, CUSTOMER_ID STRING, USAGE_DATE DATE,
                TOWER_ID STRING, VOICE_MINUTES NUMBER(10,0), DATA_USAGE_MB NUMBER(12,2),
                DATA_USAGE_GB NUMBER(12,3), SMS_COUNT NUMBER(10,0), IS_ROAMING BOOLEAN,
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_SUPPORT_TICKETS": """
            CREATE TABLE IF NOT EXISTS RAW_SUPPORT_TICKETS (
                TICKET_ID STRING, CUSTOMER_ID STRING, CATEGORY STRING,
                PRIORITY STRING, CHANNEL STRING, CREATED_AT TIMESTAMP_NTZ,
                RESOLVED_AT TIMESTAMP_NTZ, RESOLUTION_TIME_HOURS NUMBER(10,1),
                STATUS STRING, SATISFACTION_SCORE NUMBER(2,0),
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
        "RAW_NETWORK_OUTAGES": """
            CREATE TABLE IF NOT EXISTS RAW_NETWORK_OUTAGES (
                OUTAGE_ID STRING, TOWER_ID STRING, OUTAGE_START TIMESTAMP_NTZ,
                OUTAGE_END TIMESTAMP_NTZ, DURATION_MINUTES NUMBER(10,0),
                SEVERITY STRING, CAUSE STRING, ESTIMATED_IMPACTED_USERS NUMBER(10,0),
                LOAD_DATE TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            );
        """,
    }

    for tbl_name, ddl in table_ddls.items():
        cur.execute(ddl)
        print(f" - Table {tbl_name} checked/created")

    # 5. Stage Files and COPY INTO
    print("\n[Step 5/5] Uploading CSV datasets to @CRM_STAGE and executing COPY INTO...")
    file_table_mapping = [
        (CRM_SOURCE_FILE, "customer_churn.csv", "RAW_CUSTOMERS", """
            COPY INTO RAW_CUSTOMERS (
                CUSTOMER_ID, GENDER, SENIOR_CITIZEN, PARTNER, DEPENDENTS, TENURE,
                PHONE_SERVICE, MULTIPLE_LINES, INTERNET_SERVICE, ONLINE_SECURITY,
                ONLINE_BACKUP, DEVICE_PROTECTION, TECH_SUPPORT, STREAMING_TV,
                STREAMING_MOVIES, CONTRACT, PAPERLESS_BILLING, PAYMENT_METHOD,
                MONTHLY_CHARGES, TOTAL_CHARGES, CHURN
            ) FROM @CRM_STAGE/customer_churn.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (PLANS_DIR / "plans.csv", "plans.csv", "RAW_PLANS", """
            COPY INTO RAW_PLANS (
                PLAN_ID, PLAN_NAME, MONTHLY_PRICE, DATA_LIMIT_GB,
                NETWORK_TYPE, VOICE_MINUTES, SMS_LIMIT, VALIDITY_DAYS, PLAN_CATEGORY
            ) FROM @CRM_STAGE/plans.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (TOWERS_DIR / "towers.csv", "towers.csv", "RAW_TOWERS", """
            COPY INTO RAW_TOWERS (
                TOWER_ID, TOWER_NAME, CITY, STATE, LATITUDE, LONGITUDE,
                TECHNOLOGY, VENDOR, CAPACITY, INSTALLATION_DATE, STATUS
            ) FROM @CRM_STAGE/towers.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (BILLING_DIR / "customer_billing.csv", "customer_billing.csv", "RAW_BILLING", """
            COPY INTO RAW_BILLING (
                BILL_ID, CUSTOMER_ID, BILLING_PERIOD, BILL_DATE, DUE_DATE,
                BASE_AMOUNT, ADDITIONAL_CHARGES, DISCOUNT_AMOUNT, TAX_AMOUNT,
                TOTAL_AMOUNT, PAYMENT_STATUS
            ) FROM @CRM_STAGE/customer_billing.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (PAYMENTS_DIR / "customer_payments.csv", "customer_payments.csv", "RAW_PAYMENTS", """
            COPY INTO RAW_PAYMENTS (
                PAYMENT_ID, BILL_ID, CUSTOMER_ID, PAYMENT_DATETIME, AMOUNT,
                PAYMENT_METHOD, PAYMENT_GATEWAY, TRANSACTION_STATUS, TRANSACTION_REF
            ) FROM @CRM_STAGE/customer_payments.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (USAGE_DIR / "daily_usage.csv", "daily_usage.csv", "RAW_USAGE", """
            COPY INTO RAW_USAGE (
                USAGE_ID, CUSTOMER_ID, USAGE_DATE, TOWER_ID, VOICE_MINUTES,
                DATA_USAGE_MB, DATA_USAGE_GB, SMS_COUNT, IS_ROAMING
            ) FROM @CRM_STAGE/daily_usage.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (SUPPORT_DIR / "support_tickets.csv", "support_tickets.csv", "RAW_SUPPORT_TICKETS", """
            COPY INTO RAW_SUPPORT_TICKETS (
                TICKET_ID, CUSTOMER_ID, CATEGORY, PRIORITY, CHANNEL,
                CREATED_AT, RESOLVED_AT, RESOLUTION_TIME_HOURS, STATUS, SATISFACTION_SCORE
            ) FROM @CRM_STAGE/support_tickets.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
        (OUTAGES_DIR / "tower_outages.csv", "tower_outages.csv", "RAW_NETWORK_OUTAGES", """
            COPY INTO RAW_NETWORK_OUTAGES (
                OUTAGE_ID, TOWER_ID, OUTAGE_START, OUTAGE_END,
                DURATION_MINUTES, SEVERITY, CAUSE, ESTIMATED_IMPACTED_USERS
            ) FROM @CRM_STAGE/tower_outages.csv
            FILE_FORMAT = (FORMAT_NAME = CSV_FILE_FORMAT)
            ON_ERROR = 'CONTINUE';
        """),
    ]

    for local_path, stage_name, table_name, copy_sql in file_table_mapping:
        if local_path.exists():
            put_sql = f"PUT file://{local_path.resolve()} @CRM_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE"
            print(f" Uploading {local_path.name} to @CRM_STAGE...")
            cur.execute(put_sql)

            # Check if table already has rows; if not or if needed, run COPY INTO
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            existing_cnt = cur.fetchone()[0]
            if existing_cnt == 0:
                print(f" Loading data into {table_name}...")
                cur.execute(copy_sql)
            else:
                print(f" Table {table_name} already populated with {existing_cnt} rows.")
        else:
            print(f" Warning: File not found: {local_path}")

    # Row Count Verification
    print("\n" + "=" * 70)
    print("SNOWFLAKE RAW LAYER VERIFICATION SUMMARY")
    print("=" * 70)
    for _, _, table_name, _ in file_table_mapping:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        cnt = cur.fetchone()[0]
        print(f"  {table_name.ljust(25)} : {cnt:,} rows")

    cur.close()
    conn.close()
    print("=" * 70)
    print("BOOTSTRAP COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    bootstrap_snowflake()
