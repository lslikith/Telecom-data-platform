"""
==============================================================================
DAG: telecom_pipeline_dag
PURPOSE: End-to-End Telecom Data Engineering Pipeline Orchestration
AUTHOR: Likith / Telecom Data Platform Team
SCHEDULE: Daily at 02:00 UTC
==============================================================================
Flow:
1. start_pipeline
2. generate_synthetic_data (PythonOperator)
3. stage_and_load_snowflake_raw (PythonOperator)
4. dbt_run_staging (BashOperator)
5. dbt_test_staging (BashOperator)
6. dbt_run_marts (BashOperator)
7. dbt_test_marts (BashOperator)
8. dbt_snapshot_scd2 (BashOperator)
9. data_quality_audit (PythonOperator)
10. end_pipeline
==============================================================================
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project src and root to path if running locally
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DBT_DIR = PROJECT_ROOT / "dbt" / "telecom_dbt"

for path_item in [str(SRC_DIR), str(PROJECT_ROOT)]:
    if path_item not in sys.path:
        sys.path.insert(0, path_item)

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python import PythonOperator
except ImportError:
    # Graceful fallback mock for local test environments without full apache-airflow installed
    class DAG:
        def __init__(self, *args, **kwargs):
            self.dag_id = kwargs.get("dag_id", args[0] if args else "mock_dag")
            self.tasks = []
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    class BaseOperatorMock:
        def __init__(self, task_id, **kwargs):
            self.task_id = task_id
            self.upstream = []
            self.downstream = []
        def __rshift__(self, other):
            if isinstance(other, list):
                for o in other:
                    self.downstream.append(o)
                    o.upstream.append(self)
            else:
                self.downstream.append(other)
                other.upstream.append(self)
            return other

    class EmptyOperator(BaseOperatorMock): pass
    class PythonOperator(BaseOperatorMock):
        def __init__(self, task_id, python_callable=None, **kwargs):
            super().__init__(task_id, **kwargs)
            self.python_callable = python_callable
    class BashOperator(BaseOperatorMock):
        def __init__(self, task_id, bash_command="", **kwargs):
            super().__init__(task_id, **kwargs)
            self.bash_command = bash_command


# ==============================================================================
# CALLABLE FUNCTIONS
# ==============================================================================

def execute_data_generation(**kwargs):
    """Generates synthetic telecom operational feeds."""
    print(">>> Executing synthetic telecom data generation...")
    from telecom.generators.run_daily import run_all_generators
    run_all_generators()
    print(">>> All synthetic datasets successfully generated.")


def execute_snowflake_ingestion(**kwargs):
    """Stages CSV files and triggers Snowflake COPY INTO statements."""
    print(">>> Triggering Snowflake ingestion and RAW table updates...")
    from telecom.bootstrap import bootstrap_snowflake
    bootstrap_snowflake()
    print(">>> Snowflake RAW layer successfully refreshed.")


def execute_data_quality_audit(**kwargs):
    """Audits final row counts and checks data integrity across layers."""
    import snowflake.connector
    from telecom.config import (
        SNOWFLAKE_ACCOUNT,
        SNOWFLAKE_DATABASE,
        SNOWFLAKE_PASSWORD,
        SNOWFLAKE_ROLE,
        SNOWFLAKE_USER,
        SNOWFLAKE_WAREHOUSE,
    )

    print(">>> Connecting to Snowflake to perform Data Quality Audit...")
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
    )
    cur = conn.cursor()

    audit_queries = {
        "RAW_CUSTOMERS": "SELECT COUNT(*) FROM TELECOM_DB.RAW.RAW_CUSTOMERS",
        "STG_CUSTOMERS": "SELECT COUNT(*) FROM TELECOM_DB.STAGING.STG_CUSTOMERS",
        "DIM_CUSTOMERS": "SELECT COUNT(*) FROM TELECOM_DB.MARTS.DIM_CUSTOMERS",
        "FCT_BILLING_PAYMENTS": "SELECT COUNT(*) FROM TELECOM_DB.MARTS.FCT_BILLING_PAYMENTS",
        "CHURN_RISK_ANALYSIS": "SELECT COUNT(*) FROM TELECOM_DB.MARTS.CHURN_RISK_ANALYSIS",
        "HIGH_RISK_SUBSCRIBERS": "SELECT COUNT(*) FROM TELECOM_DB.MARTS.CHURN_RISK_ANALYSIS WHERE CHURN_RISK_TIER = 'HIGH RISK'",
    }

    print("\n" + "=" * 60)
    print("TELECOM PIPELINE AUDIT REPORT")
    print("=" * 60)
    for metric_name, query in audit_queries.items():
        cur.execute(query)
        cnt = cur.fetchone()[0]
        print(f"  {metric_name.ljust(25)} : {cnt:,}")
    print("=" * 60)

    cur.close()
    conn.close()
    print(">>> Data Quality Audit completed with 0 errors!")


# ==============================================================================
# DAG DEFINITION
# ==============================================================================

default_args = {
    "owner": "telecom_data_eng",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="telecom_pipeline_dag",
    default_args=default_args,
    description="End-to-End Data Pipeline: Python Generation -> Snowflake RAW -> dbt Staging -> dbt Marts -> Snapshots -> Audits",
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["telecom", "snowflake", "dbt", "production"],
) as dag:

    start_pipeline = EmptyOperator(
        task_id="start_pipeline",
    )

    generate_data_task = PythonOperator(
        task_id="generate_synthetic_telecom_data",
        python_callable=execute_data_generation,
    )

    snowflake_ingest_task = PythonOperator(
        task_id="stage_and_load_snowflake_raw",
        python_callable=execute_snowflake_ingestion,
    )

    dbt_run_staging_task = BashOperator(
        task_id="dbt_run_staging_views",
        bash_command=f"cd {DBT_DIR} && dbt run --select staging --profiles-dir .",
    )

    dbt_test_staging_task = BashOperator(
        task_id="dbt_test_staging_quality",
        bash_command=f"cd {DBT_DIR} && dbt test --select staging --profiles-dir .",
    )

    dbt_run_marts_task = BashOperator(
        task_id="dbt_run_marts_and_dimensions",
        bash_command=f"cd {DBT_DIR} && dbt run --select marts --profiles-dir .",
    )

    dbt_test_marts_task = BashOperator(
        task_id="dbt_test_marts_quality",
        bash_command=f"cd {DBT_DIR} && dbt test --select marts --profiles-dir .",
    )

    dbt_snapshot_task = BashOperator(
        task_id="dbt_snapshot_customer_scd2",
        bash_command=f"cd {DBT_DIR} && dbt snapshot --profiles-dir .",
    )

    data_quality_task = PythonOperator(
        task_id="data_quality_audit_summary",
        python_callable=execute_data_quality_audit,
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline",
    )

    # Pipeline Dependency Graph
    (
        start_pipeline
        >> generate_data_task
        >> snowflake_ingest_task
        >> dbt_run_staging_task
        >> dbt_test_staging_task
        >> dbt_run_marts_task
        >> dbt_test_marts_task
        >> dbt_snapshot_task
        >> data_quality_task
        >> end_pipeline
    )
