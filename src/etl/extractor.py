import ast
import pandas as pd
import os
from src.utils.config import JSON_FILE_PATH, CSV_FILE_PATH
from src.utils.logging import logger

def load_json_data(file_path: str = JSON_FILE_PATH) -> list[dict]:
    """
    Reads the raw JSON file line by line and parses it.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list[dict]: A list of dictionaries containing the game data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If there is an error reading the file.
    """
    logger.info(f"Loading JSON data from {file_path}...")
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    rows = []
    malformed_lines = 0
    start_time = pd.Timestamp.now()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                try:
                    rows.append(ast.literal_eval(line))
                except (ValueError, SyntaxError) as e:
                    malformed_lines += 1
                    logger.warning(f"Skipping malformed line: {e}")
                    continue
        
        end_time = pd.Timestamp.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"JSON Extraction completed in {duration:.2f} seconds.")
        logger.info(f"Total records loaded: {len(rows)}")
        logger.info(f"Malformed lines skipped: {malformed_lines}")
        return rows
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        raise

def load_csv_data(file_path: str = CSV_FILE_PATH) -> pd.DataFrame:
    """
    Reads the CSV file into a Pandas DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    logger.info(f"Loading CSV data from {file_path}...")
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded CSV with shape {df.shape}.")
        return df
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise
