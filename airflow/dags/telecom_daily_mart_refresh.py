"""
==============================================================================
DAG: telecom_daily_mart_refresh
PURPOSE: Incremental Daily Marts and Churn Risk Score Refresh
AUTHOR: Likith / Telecom Data Platform Team
SCHEDULE: Every 6 hours
==============================================================================
"""

from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DBT_DIR = PROJECT_ROOT / "dbt" / "telecom_dbt"

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
    from airflow.operators.empty import EmptyOperator
except ImportError:
    class DAG:
        def __init__(self, *args, **kwargs):
            self.dag_id = kwargs.get("dag_id", "mock_dag")
        def __enter__(self): return self
        def __exit__(self, *args): pass
    class EmptyOperator:
        def __init__(self, task_id, **kwargs): self.task_id = task_id
        def __rshift__(self, other): return other
    class BashOperator:
        def __init__(self, task_id, bash_command="", **kwargs):
            self.task_id = task_id
            self.bash_command = bash_command
        def __rshift__(self, other): return other

default_args = {
    "owner": "telecom_bi",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}

with DAG(
    dag_id="telecom_daily_mart_refresh",
    default_args=default_args,
    description="Fast refresh of analytical marts, churn risk scores, and network performance indicators",
    schedule_interval="0 */6 * * *",
    catchup=False,
    tags=["telecom", "marts", "bi", "reporting"],
) as dag:

    start = EmptyOperator(task_id="start_refresh")

    refresh_churn_risk = BashOperator(
        task_id="refresh_churn_risk_analysis",
        bash_command=f"cd {DBT_DIR} && dbt run --select churn_risk_analysis customer_churn_summary churn_by_contract --profiles-dir .",
    )

    refresh_network_marts = BashOperator(
        task_id="refresh_network_performance_marts",
        bash_command=f"cd {DBT_DIR} && dbt run --select network_performance_marts dim_towers --profiles-dir .",
    )

    test_refreshed_marts = BashOperator(
        task_id="test_refreshed_marts",
        bash_command=f"cd {DBT_DIR} && dbt test --select churn_risk_analysis network_performance_marts --profiles-dir .",
    )

    end = EmptyOperator(task_id="end_refresh")

    start >> refresh_churn_risk >> test_refreshed_marts >> end
    start >> refresh_network_marts >> test_refreshed_marts
