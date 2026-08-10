from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =====================================================
# DATASETS
# =====================================================

DATASETS = PROJECT_ROOT / "datasets"

CRM_DIR = DATASETS / "crm"

GENERATED_DIR = DATASETS / "generated"

PLANS_DIR = GENERATED_DIR / "plans"
TOWERS_DIR = GENERATED_DIR / "towers"
USAGE_DIR = GENERATED_DIR / "usage"
BILLING_DIR = GENERATED_DIR / "billing"
PAYMENTS_DIR = GENERATED_DIR / "payments"
SUPPORT_DIR = GENERATED_DIR / "support"
OUTAGES_DIR = GENERATED_DIR / "outages"

CRM_FILE = CRM_DIR / "WA_Fn-UseC_-Telco-Customer-Churn.csv"

# =====================================================
# GENERATION SETTINGS
# =====================================================

TOTAL_TOWERS = 500

USAGE_RECORDS_PER_DAY = 500000

SUPPORTED_NETWORKS = ["4G", "5G"]

VENDORS = [
    "Ericsson",
    "Nokia",
    "Samsung",
    "Huawei"
]