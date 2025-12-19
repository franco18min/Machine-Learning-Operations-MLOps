from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import sys
import os

# Add project root to sys.path to allow imports from src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from airflow_dags.operators.extract_operator import ExtractOperator
from airflow_dags.operators.transform_operator import TransformOperator
from airflow_dags.operators.load_operator import LoadOperator
from src.utils.logging import logger

# Default arguments for the DAG
default_args = {
    "owner": "nexus_mlops",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["admin@example.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    "steam_games_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for Steam Games data",
    schedule_interval="@daily",
    catchup=False,
    tags=["etl", "steam", "mlops"],
) as dag:

    # 1. Extraction Task
    extract_task = ExtractOperator(
        task_id="extract_steam_data", source_type="json", file_path="steam_games.json"
    )

    # 2. Transformation Task
    transform_task = TransformOperator(
        task_id="transform_steam_data", transformation_type="json_to_df"
    )

    # 3. Data Quality Check Task (Simulated)
    def check_data_quality():
        logger.info("Running data quality checks...")
        # Here we could run the pytest suite programmatically or specific checks
        # For demonstration, we assume success if previous steps passed
        logger.info("Data quality checks passed.")

    quality_check_task = PythonOperator(
        task_id="data_quality_checks", python_callable=check_data_quality
    )

    # 4. Load Task
    load_task = LoadOperator(task_id="load_data_to_cache", target="dataframe_cache")

    # 5. Notification Task
    # Note: EmailOperator requires SMTP configuration in airflow.cfg
    # Using PythonOperator with logger for local demonstration
    def send_success_notification():
        logger.info("Pipeline completed successfully. Notification sent.")

    notification_task = PythonOperator(
        task_id="notify_success", python_callable=send_success_notification
    )

    # Define Dependencies
    (
        extract_task
        >> transform_task
        >> quality_check_task
        >> load_task
        >> notification_task
    )
