import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset Directories
DATASETS = PROJECT_ROOT / "datasets"
SOURCE_DIR = DATASETS / "source"
RAW_DIR = DATASETS / "raw"
MASTER_DIR = DATASETS / "master"
GENERATED_DIR = DATASETS / "generated"

# Sub-directories under Generated
BILLING_DIR = GENERATED_DIR / "billing"
OUTAGES_DIR = GENERATED_DIR / "outages"
PAYMENTS_DIR = GENERATED_DIR / "payments"
PLANS_DIR = GENERATED_DIR / "plans"
SUPPORT_DIR = GENERATED_DIR / "support"
TOWERS_DIR = GENERATED_DIR / "towers"
USAGE_DIR = GENERATED_DIR / "usage"

# Source & Raw Files
CRM_SOURCE_FILE = SOURCE_DIR / "crm" / "customer_churn.csv"
CRM_FILE = CRM_SOURCE_FILE

# Generation Volume Constants
TOTAL_TOWERS = 100
SAMPLE_CUSTOMERS_COUNT = 5000

# Snowflake Default Configurations
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "AVQXGPE-JC49269")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "LIKITH")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "Likithliki@9535")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "TELECOM_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "TELECOM_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")