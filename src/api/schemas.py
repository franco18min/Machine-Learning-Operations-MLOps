from pydantic import BaseModel
from typing import Dict, List, Union


class TopGenresResponse(BaseModel):
    top_genres: Dict[str, int]


class GamesResponse(BaseModel):
    games: List[str]


class TopSpecsResponse(BaseModel):
    top_specs: Dict[str, int]


class EarlyAccessResponse(BaseModel):
    games: int


class SentimentResponse(BaseModel):
    sentiment: Dict[str, int]


class TopGamesItem(BaseModel):
    title: str
    metascore: Union[float, int]


class TopGamesResponse(BaseModel):
    top_games: List[TopGamesItem]


class PredictionResponse(BaseModel):
    price: float
    rmse: float
