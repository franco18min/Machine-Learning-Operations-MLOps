from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from src.etl.loader import get_games_dataframe
from src.utils.logging import logger

class LoadOperator(BaseOperator):
    """
    Custom Airflow Operator to load transformed data into destination (Cache/DB).
    """

    @apply_defaults
    def __init__(self, target: str, *args, **kwargs):
        super(LoadOperator, self).__init__(*args, **kwargs)
        self.target = target

    def execute(self, context):
        logger.info(f"Starting load to target: {self.target}")
        
        try:
            # Simulate loading by calling the loader function which caches data
            # In a real scenario, this would write to Postgres/BigQuery
            df = get_games_dataframe()
            logger.info(f"Successfully loaded {len(df)} records into application cache/memory.")
            return "load_success"

        except Exception as e:
            logger.error(f"Load failed: {e}")
            raise
