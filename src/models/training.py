import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from src.etl.loader import get_training_data
from src.etl.transformer import clean_data_for_training
from src.utils.logging import logger


def train_and_predict_price(
    release_year: int, early_access: bool, metascore: float
) -> dict[str, float]:
    """
    Trains a Linear Regression model on the fly and predicts the price for a given game.

    Args:
        release_year (int): The year the game was released.
        early_access (bool): Whether the game is in early access.
        metascore (float): The metascore of the game.

    Returns:
        dict[str, float]: A dictionary containing the predicted price and the RMSE of the model.
    """
    logger.info(
        f"Starting prediction for: Year={release_year}, EarlyAccess={early_access}, Metascore={metascore}"
    )

    try:
        # Load raw data
        df_raw = get_training_data()

        # Clean and prepare data
        X, y = clean_data_for_training(df_raw)

        # One-Hot Encoding for categorical features (though current features are mostly numeric/bool)
        # pd.get_dummies is used in original code, so we keep it for consistency if X has categoricals.
        # In the original code, X had 'release_year', 'early_access', 'metascore'.
        # 'early_access' is boolean/categorical. 'release_year' is int but treated as numeric in regression usually.
        X = pd.get_dummies(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)
        logger.info("Model trained successfully.")

        # Evaluate model
        y_pred = model.predict(X_test)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5
        logger.info(f"Model RMSE: {rmse}")

        # Prepare input for prediction
        input_features = pd.DataFrame(
            {
                "release_year": [release_year],
                "early_access": [early_access],
                "metascore": [metascore],
            }
        )

        # Ensure dummy columns match training data
        input_features = pd.get_dummies(input_features)
        input_features = input_features.reindex(columns=X.columns, fill_value=0)

        # Predict
        price = model.predict(input_features)[0]
        logger.info(f"Predicted Price: {price}")

        return {"price": float(price), "rmse": float(rmse)}

    except Exception as e:
        logger.error(f"Error in training/prediction process: {e}")
        raise
