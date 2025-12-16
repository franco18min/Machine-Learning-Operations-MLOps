from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from src.etl.extractor import load_json_data, load_csv_data
from src.utils.logging import logger

class ExtractOperator(BaseOperator):
    """
    Custom Airflow Operator to extract data from JSON or CSV sources.
    """

    @apply_defaults
    def __init__(self, source_type: str, file_path: str, *args, **kwargs):
        super(ExtractOperator, self).__init__(*args, **kwargs)
        self.source_type = source_type
        self.file_path = file_path

    def execute(self, context):
        logger.info(f"Starting extraction for source: {self.source_type}")
        
        try:
            if self.source_type == 'json':
                data = load_json_data(self.file_path)
                logger.info(f"Extracted {len(data)} records from JSON.")
                # In a real Airflow setup, we would push this to XCom or save to a staging area (S3/GCS/Local)
                # For this local simulation, we'll just return a summary string
                return f"extracted_json_{len(data)}"
            
            elif self.source_type == 'csv':
                df = load_csv_data(self.file_path)
                logger.info(f"Extracted dataframe with shape {df.shape} from CSV.")
                return f"extracted_csv_{df.shape[0]}"
            
            else:
                raise ValueError(f"Unsupported source type: {self.source_type}")
                
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise
