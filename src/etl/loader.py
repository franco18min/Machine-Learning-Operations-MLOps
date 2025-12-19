import pandas as pd
from src.etl.extractor import load_json_data, load_csv_data
from src.etl.transformer import transform_json_to_dataframe
from src.utils.logging import logger

# Global cache for the DataFrame to avoid reloading on every request if desired
# Though for this assignment, keeping it simple.
_GAMES_DF = None


def get_games_dataframe() -> pd.DataFrame:
    """
    Orchestrates the loading and transformation of the games data (JSON).
    Returns the main DataFrame used for API queries.
    Uses a global variable to cache the data in memory.

    Returns:
        pd.DataFrame: The main games DataFrame.
    """
    global _GAMES_DF
    if _GAMES_DF is not None:
        return _GAMES_DF

    logger.info("Initializing games data pipeline...")
    try:
        start_time = pd.Timestamp.now()
        raw_data = load_json_data()
        df = transform_json_to_dataframe(raw_data)
        _GAMES_DF = df

        end_time = pd.Timestamp.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"Games data pipeline completed in {duration:.2f} seconds.")
        logger.info(f"Pipeline Success: Loaded {len(df)} records.")

        return df
    except Exception as e:
        logger.critical(f"Failed to initialize games data: {e}")
        raise


def get_training_data() -> pd.DataFrame:
    """
    Loads the CSV data for training.

    Returns:
        pd.DataFrame: The raw DataFrame from CSV.
    """
    return load_csv_data()
