# 📡 Telecom Data Platform — End-to-End Enterprise Lakehouse & Analytics

[![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Cloud-29B5E8?logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![dbt](https://img.shields.io/badge/dbt-1.10.13-FF694B?logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.2-017CEE?logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

An enterprise-grade, end-to-end data platform simulating a real-world telecommunications analytics lakehouse. The platform ingests customer CRM, radio access network (RAN) cell towers, billing cycles, payment transactions, subscriber cellular usage, customer service tickets, and network outages into **Snowflake**, transforms and models data into conformed dimensions and marts using **dbt**, and automates pipeline execution with **Apache Airflow**.

---

## 🏛️ Architecture Overview

```mermaid
flowchart TD
    subgraph IngestionLayer ["1. Ingestion & Synthetic Feeds (Python)"]
        CRM["Customer CRM Data\n(7,043 Subscribers)"]
        GEN["Python Generators\nPlans, Towers, Billing, Payments,\nUsage, Support Tickets, Outages"]
        BOOTSTRAP["Bootstrap & Ingestion Engine\ntelecom.bootstrap / ingest_crm"]
        CRM --> BOOTSTRAP
        GEN --> BOOTSTRAP
    end

    subgraph StorageLayer ["2. Cloud Lakehouse (Snowflake RAW)"]
        STAGE["Snowflake Stage\n@CRM_STAGE"]
        BOOTSTRAP -->|PUT & COPY INTO| STAGE
        RAW_DB[("TELECOM_DB.RAW\nRAW_CUSTOMERS (7,043)\nRAW_BILLING (21,129)\nRAW_PAYMENTS (19,488)\nRAW_USAGE (11,936)\nRAW_SUPPORT_TICKETS (3,500)\nRAW_NETWORK_OUTAGES (250)\nRAW_TOWERS (100)\nRAW_PLANS (7)")]
        STAGE --> RAW_DB
    end

    subgraph DbtLayer ["3. Transformation Layer (dbt Core)"]
        STG[("STAGING Layer (Views)\nstg_customers, stg_billing, stg_payments,\nstg_usage, stg_support_tickets,\nstg_towers, stg_plans, stg_outages")]
        SNAP[("SNAPSHOTS (SCD Type 2)\nsnap_customers (Contract & Churn Tracking)")]
        MARTS[("MARTS Layer (Tables)\ndim_customers, dim_plans, dim_towers\nfct_billing_payments, fct_daily_usage\nfct_support_tickets, churn_risk_analysis\nchurn_by_contract, customer_churn_summary\nnetwork_performance_marts")]
        TESTS["dbt Data Tests (93 Tests)\nSchema, Accepted Values, Uniqueness, Singular Business Tests"]

        RAW_DB --> STG
        RAW_DB --> SNAP
        STG --> MARTS
        MARTS --> TESTS
    end

    subgraph OrchestrationLayer ["4. Orchestration (Apache Airflow)"]
        DAG["telecom_pipeline_dag (@daily)\nData Gen ➔ Snowflake Load ➔ dbt Staging ➔ dbt Marts ➔ SCD2 ➔ Quality Audit"]
        REFRESH_DAG["telecom_daily_mart_refresh (every 6h)\nIncremental Marts & Churn Scoring Refresh"]
    end

    DAG -.-> IngestionLayer
    DAG -.-> StorageLayer
    DAG -.-> DbtLayer

    subgraph AnalyticsLayer ["5. BI & Analytics"]
        BI["Executive Dashboards & BI\n• Churn Prediction & Risk Scoring (1,150 High Risk)\n• ARPU & Lifetime Value Analysis\n• Tower Reliability & Network Outages\n• Customer Support CSAT Analysis"]
        MARTS --> BI
    end
```

---

## 🛠️ Tech Stack & Responsibilities

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Data Warehouse** | **Snowflake** | Cloud data storage, compute (`TELECOM_WH`), stages, and multi-schema separation (`RAW`, `STAGING`, `MARTS`). |
| **Transformations** | **dbt Core (1.10.13)** | Modular SQL transformations, conformed dimensional modeling, SCD Type 2 history snapshots, schema testing, and documentation. |
| **Orchestration** | **Apache Airflow (2.8+)** | Workflow scheduling, automated DAG task orchestration, data quality audits, Docker Compose infrastructure. |
| **Data Generation** | **Python (3.9+) & Pandas** | High-fidelity synthetic telecom data generators (plans, cell towers, usage events, support tickets, billing invoices, network outages). |
| **Version Control** | **Git & GitHub** | Infrastructure-as-code, CI/CD ready repository structure. |

---

## 📂 Project Directory Structure

```text
Telecom-data-platform/
│
├── README.md                      # Comprehensive platform architecture & operational guide
├── datasets/                      # Seed & generated telecom datasets
│   ├── source/crm/                # Base customer churn CRM dataset
│   ├── master/                    # Master reference data (vendors, cities, circles, plans)
│   ├── raw/crm/                   # Ingested timestamped files
│   └── generated/                 # Synthetic generator output
│       ├── billing/               # Monthly subscriber bills
│       ├── outages/               # Tower downtime & outages
│       ├── payments/              # Payment transaction logs
│       ├── plans/                 # 4G/5G/Fiber plan definitions
│       ├── support/               # Customer service tickets
│       ├── towers/                # Cell tower RAN network data
│       └── usage/                 # Daily voice/data/SMS records
│
├── sql/                           # Modular Snowflake SQL Infrastructure Scripts
│   ├── README.md                  # Snowflake execution guide
│   ├── 00_environment_setup.sql   # Warehouse, DB, schemas, role definitions
│   ├── 01_file_formats.sql        # Standardized CSV file format
│   ├── 02_stages.sql              # Internal & external stage definitions
│   ├── 03_raw_tables.sql          # DDL for all 8 RAW layer tables
│   ├── 04_copy_into.sql           # COPY INTO statements with error handling
│   ├── 05_validation.sql          # Data audits, table row counts & PK verification
│   ├── 06_queries.sql             # Business intelligence & analytical queries
│   ├── 07_storage_integrations.sql# AWS S3 IAM Role integration
│   └── 08_external_stage.sql      # External S3 bucket stage
│
├── dbt/telecom_dbt/               # Production dbt Project
│   ├── dbt_project.yml            # Project configuration & schema routing
│   ├── packages.yml               # dbt-utils package dependencies
│   ├── profiles.yml               # Portable Snowflake profile config with env vars
│   ├── macros/
│   │   └── generate_schema_name.sql # Custom schema name router (STAGING / MARTS)
│   ├── models/
│   │   ├── schema.yml             # Data dictionary, column descriptions & tests
│   │   ├── overview.md            # dbt documentation overview page
│   │   ├── staging/               # Silver Layer Views
│   │   │   ├── sources.yml        # Source declarations & freshness/uniqueness tests
│   │   │   ├── stg_customers.sql  # Normalized customer demographics & contracts
│   │   │   ├── stg_plans.sql      # Plan pricing & allowances
│   │   │   ├── stg_towers.sql     # Cell tower infrastructure & coordinates
│   │   │   ├── stg_billing.sql    # Billing cycle statements
│   │   │   ├── stg_payments.sql   # Payment transactions & gateway status
│   │   │   ├── stg_usage.sql      # Daily subscriber usage metrics
│   │   │   ├── stg_support_tickets.sql # Service desk tickets & CSAT
│   │   │   └── stg_network_outages.sql # Outage incidents & impacted subscribers
│   │   └── marts/                 # Gold Layer Tables & Analytics
│   │       ├── dim_customers.sql  # Conformed customer dimension + cohorts
│   │       ├── dim_plans.sql      # Plan dimension
│   │       ├── dim_towers.sql     # Tower dimension with calculated uptime %
│   │       ├── fct_billing_payments.sql # Billing fulfillment & delinquency fact
│   │       ├── fct_daily_usage.sql# Cellular data & voice consumption fact
│   │       ├── fct_support_tickets.sql # Service issues & resolution turnaround fact
│   │       ├── churn_by_contract.sql   # Churn rate by contract type
│   │       ├── customer_churn_summary.sql # Executive churn KPI summary
│   │       ├── churn_risk_analysis.sql # Multi-factor predictive churn risk scoring
│   │       └── network_performance_marts.sql # Tower utilization & reliability mart
│   ├── snapshots/
│   │   └── snap_customers.sql     # SCD Type 2 customer contract & churn tracker
│   └── tests/                     # Singular Custom Business Tests
│       ├── assert_positive_billing_amounts.sql
│       ├── assert_valid_churn_flags.sql
│       └── assert_no_negative_usage.sql
│
├── airflow/                       # Apache Airflow Orchestration
│   ├── README.md                  # Setup & execution instructions
│   ├── docker-compose.yaml        # Airflow 2.8+ containerized stack with Postgres
│   ├── test_airflow_dags.py       # Standalone DAG syntax & integrity test runner
│   └── dags/
│       ├── telecom_pipeline_dag.py        # Master Daily End-to-End Pipeline DAG
│       └── telecom_daily_mart_refresh.py  # 6-Hour Marts & Churn Score Refresh DAG
│
└── src/telecom/                   # Python Core Package
    ├── config.py                  # Environment paths & Snowflake credentials
    ├── common.py                  # Shared utilities & customer loader
    ├── bootstrap.py               # 1-Command Snowflake provisioning & data loader
    ├── ingestion/
    │   └── ingest_crm.py          # CRM file timestamped ingest
    └── generators/
        ├── run_daily.py           # Master generator suite runner
        ├── master_data.py         # Vendors, cities, circles, plans generator
        ├── plans.py               # Mobile & broadband plan generator
        ├── towers.py              # Cell tower RAN network generator
        ├── billing.py             # Monthly customer billing cycle generator
        ├── payments.py            # Transaction receipts & payment gateway generator
        ├── usage.py               # Cellular voice, data GB, SMS usage generator
        ├── support.py             # Customer care tickets & CSAT generator
        └── outages.py             # Tower outage & downtime incident generator
```

---

## 🚀 Step-by-Step Setup & Execution

### 1. Prerequisites
- macOS / Linux / Windows WSL
- Python 3.9+ with virtual environment
- Snowflake Account with `ACCOUNTADMIN` or equivalent privileges

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/lslikith/Telecom-data-platform.git
cd Telecom-data-platform

# Activate Python virtual environment & install requirements
python3 -m venv .venv
source .venv/bin/activate
pip install snowflake-connector-python pandas dbt-snowflake dbt-core
```

### 3. Generate Synthetic Feeds & Provision Snowflake
Run the one-command bootstrap to generate all synthetic datasets, provision Snowflake warehouse/database/schemas, upload files to the Snowflake internal stage, and populate the RAW tables:

```bash
PYTHONPATH=src python src/telecom/bootstrap.py
```

**Output Verification**:
```text
SNOWFLAKE RAW LAYER VERIFICATION SUMMARY
======================================================================
  RAW_CUSTOMERS             : 7,043 rows
  RAW_PLANS                 : 7 rows
  RAW_TOWERS                : 100 rows
  RAW_BILLING               : 21,129 rows
  RAW_PAYMENTS              : 19,488 rows
  RAW_USAGE                 : 11,936 rows
  RAW_SUPPORT_TICKETS       : 3,500 rows
  RAW_NETWORK_OUTAGES       : 250 rows
======================================================================
BOOTSTRAP COMPLETED SUCCESSFULLY!
```

---

### 4. dbt Transformations, Tests & Documentation

Navigate to the dbt project:
```bash
cd dbt/telecom_dbt
```

1. **Install dbt dependencies**:
   ```bash
   dbt deps --profiles-dir .
   ```

2. **Run all staging views and marts tables**:
   ```bash
   dbt run --profiles-dir .
   ```
   *(Builds 8 views in `STAGING` and 11 tables in `MARTS` with 100% success)*.

3. **Execute SCD Type 2 Snapshots**:
   ```bash
   dbt snapshot --profiles-dir .
   ```
   *(Captures historical customer contract and churn state transitions)*.

4. **Execute All Schema and Singular Tests**:
   ```bash
   dbt test --profiles-dir .
   ```
   *(Runs 93 comprehensive tests: 100% pass, 0 warnings, 0 errors)*.

5. **Generate dbt Documentation**:
   ```bash
   dbt docs generate --profiles-dir .
   dbt docs serve --profiles-dir .
   ```

---

### 5. Apache Airflow Orchestration

#### Option A: Running with Docker Compose
```bash
cd airflow
docker compose up airflow-init
docker compose up -d
```
Access the Airflow Webserver at `http://localhost:8080` (user: `admin`, password: `admin`).

#### Option B: Standalone DAG Verification (No Docker Needed)
Validate DAG syntax, task dependencies, and run a live Snowflake data quality audit directly:
```bash
python airflow/test_airflow_dags.py
```

---

## 📊 Business Intelligence & Analytics Showcase

### 1. Customer Churn by Contract Type
Month-to-month subscribers exhibit the highest churn vulnerability (~42.7%), whereas Two-year contracts yield minimal churn (~2.8%).
```sql
SELECT 
    CONTRACT,
    TOTAL_CUSTOMERS,
    CHURNED_CUSTOMERS,
    ACTIVE_CUSTOMERS,
    CHURN_RATE_PERCENT
FROM TELECOM_DB.MARTS.CHURN_BY_CONTRACT
ORDER BY CHURN_RATE_PERCENT DESC;
```

### 2. Multi-Factor Churn Risk Tiering
Subscribers are dynamically assigned a Churn Risk Score (0-100) based on contract duration, tenure, overdue payments, and customer care complaints:
```sql
SELECT 
    CHURN_RISK_TIER,
    COUNT(*) AS SUBSCRIBER_COUNT,
    ROUND(AVG(CHURN_RISK_SCORE), 1) AS AVG_RISK_SCORE,
    ROUND(AVG(MONTHLY_CHARGES), 2) AS AVG_MONTHLY_CHARGES,
    SUM(CHURN_FLAG) AS ACTUAL_CHURNED
FROM TELECOM_DB.MARTS.CHURN_RISK_ANALYSIS
GROUP BY CHURN_RISK_TIER
ORDER BY AVG_RISK_SCORE DESC;
```
*Current Analysis: Identifies **1,150 high-risk subscribers** enabling proactive customer retention campaigns.*

### 3. Cell Tower Uptime & Subscriber Impact
Correlates cell tower maintenance, hardware failures, and weather incidents with network availability:
```sql
SELECT 
    CITY,
    TECHNOLOGY,
    COUNT(TOWER_ID) AS TOWER_COUNT,
    ROUND(AVG(UPTIME_AVAILABILITY_PCT), 2) AS AVG_AVAILABILITY_PCT,
    SUM(TOTAL_DOWNTIME_MINUTES) AS TOTAL_DOWNTIME_MINS,
    SUM(TOTAL_SUBSCRIBERS_IMPACTED) AS IMPACTED_SUBSCRIBERS
FROM TELECOM_DB.MARTS.DIM_TOWERS
GROUP BY CITY, TECHNOLOGY
ORDER BY TOTAL_DOWNTIME_MINS DESC;
```

---

## 🧪 Validation & Testing Summary

- ✅ **Python Generators**: Verified across 8 synthetic domains generating 58,000+ realistic operational records in < 2 seconds.
- ✅ **Snowflake RAW Layer**: 8 tables provisioned, staged, and loaded via idempotent COPY INTO statements.
- ✅ **dbt Models**: 19 models compiled and executed into dedicated `STAGING` and `MARTS` schemas.
- ✅ **dbt Snapshots**: SCD Type 2 snapshot tracking customer changes over time with `check` strategy.
- ✅ **dbt Tests**: **93 tests passed with 100% success** (0 failures, 0 warnings).
- ✅ **Airflow DAGs**: 2 production DAGs verified with acyclic dependency checks and live audit task execution.

---

## 👤 Author & Attribution

- **Engineer**: Likith ([@lslikith](https://github.com/lslikith))
- **Repository**: [https://github.com/lslikith/Telecom-data-platform](https://github.com/lslikith/Telecom-data-platform)
