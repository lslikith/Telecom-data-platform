from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset folders
DATASETS = PROJECT_ROOT / "datasets"

SOURCE_DIR = DATASETS / "source"
RAW_DIR = DATASETS / "raw"
MASTER_DIR = DATASETS / "master"
GENERATED_DIR = DATASETS / "generated"

# Source Files
CRM_FILE = SOURCE_DIR / "crm" / "customer_churn.csv"