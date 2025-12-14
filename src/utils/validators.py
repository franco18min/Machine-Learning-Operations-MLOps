from typing import Any
import pandas as pd

def validate_year(year: str) -> bool:
    """
    Validates if the input string is a valid year format (YYYY).

    Args:
        year (str): The year string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    return year.isdigit() and len(year) == 4

def validate_dataframe(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """
    Checks if a DataFrame contains the required columns.

    Args:
        df (pd.DataFrame): The DataFrame to check.
        required_columns (list[str]): List of column names that must exist.

    Returns:
        bool: True if all columns exist, False otherwise.
    """
    return all(col in df.columns for col in required_columns)
