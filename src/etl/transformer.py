import pandas as pd
from src.utils.logging import logger


def transform_json_to_dataframe(data: list[dict]) -> pd.DataFrame:
    """
    Converts a list of dictionaries to a Pandas DataFrame.

    Args:
        data (list[dict]): The raw data.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    logger.info("Transforming raw data to DataFrame...")
    try:
        df = pd.DataFrame(data)
        logger.info(f"DataFrame created with shape {df.shape}.")
        return df
    except Exception as e:
        logger.error(f"Error transforming data to DataFrame: {e}")
        raise


def clean_data_for_training(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepares the DataFrame for training the Linear Regression model.
    Selects features, drops nulls, and separates target variable.

    Args:
        df (pd.DataFrame): The raw input DataFrame (from CSV).

    Returns:
        tuple[pd.DataFrame, pd.Series]: Features (X) and Target (y).
    """
    logger.info("Cleaning data for training...")
    try:
        # Select features and target
        # Based on model.py logic: X = df[['release_year', 'early_access', 'metascore']], y = df['price']
        required_cols = ["release_year", "early_access", "metascore", "price"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"DataFrame missing required columns: {required_cols}")

        X = df[["release_year", "early_access", "metascore"]]
        y = df["price"]

        # Drop rows with missing values in features
        # Note: model.py did X.dropna() then y = y[X.index].
        # Better to concat, dropna, then split to ensure alignment.
        combined = pd.concat([X, y], axis=1)
        original_len = len(combined)
        combined_clean = combined.dropna()
        dropped_len = original_len - len(combined_clean)

        if dropped_len > 0:
            logger.info(f"Dropped {dropped_len} rows with missing values.")

        X_clean = combined_clean[["release_year", "early_access", "metascore"]]
        y_clean = combined_clean["price"]

        logger.info(
            f"Data cleaning complete. Final training set size: {len(X_clean)} rows."
        )
        return X_clean, y_clean

    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise
