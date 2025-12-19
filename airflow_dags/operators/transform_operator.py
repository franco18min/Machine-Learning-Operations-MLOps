from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from src.etl.transformer import transform_json_to_dataframe, clean_data_for_training
from src.etl.extractor import (
    load_json_data,
    load_csv_data,
)  # Needed to simulate data flow if not using XCom fully
from src.utils.logging import logger


class TransformOperator(BaseOperator):
    """
    Custom Airflow Operator to transform raw data.
    """

    @apply_defaults
    def __init__(self, transformation_type: str, *args, **kwargs):
        super(TransformOperator, self).__init__(*args, **kwargs)
        self.transformation_type = transformation_type

    def execute(self, context):
        logger.info(f"Starting transformation: {self.transformation_type}")

        try:
            if self.transformation_type == "json_to_df":
                # In real Airflow, retrieve data from previous task via XCom or staging
                # Here we simulate by reloading (inefficient but works for structure demo)
                raw_data = load_json_data()
                df = transform_json_to_dataframe(raw_data)
                logger.info(f"Transformed to DataFrame with shape {df.shape}")
                return "transformation_success"

            elif self.transformation_type == "clean_training_data":
                df_raw = load_csv_data()
                X, y = clean_data_for_training(df_raw)
                logger.info(
                    f"Cleaned training data. X shape: {X.shape}, y shape: {y.shape}"
                )
                return "cleaning_success"

            else:
                raise ValueError(
                    f"Unsupported transformation type: {self.transformation_type}"
                )

        except Exception as e:
            logger.error(f"Transformation failed: {e}")
            raise
