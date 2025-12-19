from fastapi import APIRouter, HTTPException, Query
from src.etl.loader import get_games_dataframe
from src.models.training import train_and_predict_price
from src.api.schemas import (
    TopGenresResponse,
    GamesResponse,
    TopSpecsResponse,
    EarlyAccessResponse,
    SentimentResponse,
    TopGamesResponse,
    PredictionResponse,
)
from src.utils.logging import logger
import pandas as pd

router = APIRouter()


@router.get("/genres/{generos}", response_model=TopGenresResponse)
def genres(year: str):
    """
    Returns the top 5 genres for a given year.
    """
    try:
        df = get_games_dataframe()
        mask = df["release_date"].str.startswith(year, na=False)
        df_year = df[mask]

        if df_year.empty:
            logger.warning(f"No games found for year {year}")
            return {"top_genres": {}}

        top_genres = df_year["genres"].explode().value_counts().head(5).to_dict()
        return {"top_genres": top_genres}
    except Exception as e:
        logger.error(f"Error in genres endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/games/{juegos}", response_model=GamesResponse)
def games(year: str):
    """
    Returns the list of games released in a given year.
    """
    try:
        df = get_games_dataframe()
        mask = df["release_date"].str.startswith(year, na=False)
        df_year = df[mask]

        games_list = df_year["title"].explode().value_counts().index.tolist()
        return {"games": games_list}
    except Exception as e:
        logger.error(f"Error in games endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/specs/{especificaciones}", response_model=TopSpecsResponse)
def specs(year: str):
    """
    Returns the top 5 specs for a given year.
    """
    try:
        df = get_games_dataframe()
        mask = df["release_date"].str.startswith(year, na=False)
        df_year = df[mask]

        top_specs = df_year["specs"].explode().value_counts().head(5).to_dict()
        return {"top_specs": top_specs}
    except Exception as e:
        logger.error(f"Error in specs endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get(
    "/games_early_access/{juegos_acceso_anticipado}", response_model=EarlyAccessResponse
)
def early_access(year: str):
    """
    Returns the count of games with early access in a given year.
    """
    try:
        df = get_games_dataframe()
        mask = (df["release_date"].str.startswith(year, na=False)) & (
            df["early_access"] == True
        )
        df_year = df[mask]
        games_count = len(df_year)
        return {"games": games_count}
    except Exception as e:
        logger.error(f"Error in early_access endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/sentiment/{sentimiento}", response_model=SentimentResponse)
def sentiment(year: str):
    """
    Returns the distribution of sentiment analysis for a given year.
    """
    try:
        df = get_games_dataframe()
        mask = df["release_date"].str.startswith(year, na=False)
        df_year = df[mask]
        sentiment_dict = df_year["sentiment"].value_counts().to_dict()
        return {"sentiment": sentiment_dict}
    except Exception as e:
        logger.error(f"Error in sentiment endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/top_games/{top_juegos}", response_model=TopGamesResponse)
def top_games(year: str):
    """
    Returns the top 5 games by metascore for a given year.
    """
    try:
        df = get_games_dataframe()
        mask = df["release_date"].str.startswith(year, na=False)
        df_year = df[mask]

        # Ensure metascore is numeric for sorting
        # Creating a copy to avoid SettingWithCopyWarning on cached DF
        df_year = df_year.copy()
        df_year["metascore"] = pd.to_numeric(df_year["metascore"], errors="coerce")

        top_games_list = (
            df_year.sort_values(by="metascore", ascending=False)
            .head(5)[["title", "metascore"]]
            .to_dict("records")
        )
        return {"top_games": top_games_list}
    except Exception as e:
        logger.error(f"Error in top_games endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/prediction_price/{prediccion_precio}", response_model=PredictionResponse)
def prediction_price(
    release_year: int = Query(..., description="Year of release"),
    earlyaccess: bool = Query(..., description="Is Early Access?"),
    metascore: float = Query(..., description="Metascore"),
):
    """
    Predicts the price of a game based on features.
    """
    try:
        result = train_and_predict_price(release_year, earlyaccess, metascore)
        return result
    except Exception as e:
        logger.error(f"Error in prediction_price endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
