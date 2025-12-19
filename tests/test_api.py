from fastapi.testclient import TestClient
from src.api.main import app
import pytest

client = TestClient(app)


def test_root():
    """Test the documentation root (FastAPI default docs are at /docs, but root / might be 404)."""
    response = client.get("/")
    assert response.status_code in [200, 404]  # Depending on if root is defined


def test_genres_endpoint():
    """Test /genres/{generos} endpoint."""
    # Based on code: path param {generos} is required, query param year is required
    response = client.get("/genres/action?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert "top_genres" in data
    assert isinstance(data["top_genres"], dict)


def test_games_endpoint():
    """Test /games/{juegos} endpoint."""
    response = client.get("/games/anything?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data
    assert isinstance(data["games"], list)


def test_specs_endpoint():
    """Test /specs/{especificaciones} endpoint."""
    response = client.get("/specs/anything?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert "top_specs" in data
    assert isinstance(data["top_specs"], dict)


def test_early_access_endpoint():
    """Test /games_early_access/{juegos_acceso_anticipado} endpoint."""
    response = client.get("/games_early_access/anything?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert "games" in data
    assert isinstance(data["games"], int)


def test_sentiment_endpoint():
    """Test /sentiment/{sentimiento} endpoint."""
    response = client.get("/sentiment/anything?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert isinstance(data["sentiment"], dict)


def test_top_games_endpoint():
    """Test /top_games/{top_juegos} endpoint."""
    response = client.get("/top_games/anything?year=2010")
    assert response.status_code == 200
    data = response.json()
    assert "top_games" in data
    assert isinstance(data["top_games"], list)


def test_prediction_price_endpoint():
    """Test /prediction_price/{prediccion_precio} endpoint."""
    # Function signature: def prediction_price(release_year: int, earlyaccess: bool, metascore: float):
    # Path param: {prediccion_precio}
    # Query params: release_year, earlyaccess, metascore
    response = client.get(
        "/prediction_price/anything?release_year=2010&earlyaccess=false&metascore=80.5"
    )
    assert response.status_code == 200
    data = response.json()
    assert "price" in data
    assert "rmse" in data


def test_api_error_handling():
    """Test basic error handling (missing query params)."""
    # Missing year
    response = client.get("/genres/action")
    assert response.status_code == 422  # Validation error
