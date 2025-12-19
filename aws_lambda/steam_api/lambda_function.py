"""
Steam Games API - Lambda Function URL
Expone endpoints para consultar datos de DynamoDB
100% GRATIS - Usa Lambda Function URL (no API Gateway)
"""

import json
import boto3
from decimal import Decimal
from urllib.parse import parse_qs
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("steam_games")


def decimal_default(obj):
    """Convierte Decimal a float para JSON"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def parse_query_string(event):
    """Parse query string desde Lambda Function URL"""
    raw_query = event.get("rawQueryString", "")

    if not raw_query:
        return {}

    params = {}
    for param in raw_query.split("&"):
        if "=" in param:
            key, value = param.split("=", 1)
            params[key] = value

    return params


def lambda_handler(event, context):
    """
    Handler para Lambda Function URL

    Rutas:
    GET / → health check
    GET /?year=2023 → juegos por año
    GET /?genre=Action → juegos por género
    GET /?top=true → top 10 juegos más caros
    """

    try:
        # Obtener path y query params
        path = event.get("rawPath", "/")
        http_method = (
            event.get("requestContext", {}).get("http", {}).get("method", "GET")
        )
        query_params = parse_query_string(event)

        logger.info(f"Endpoint: {http_method} {path}")
        logger.info(f"Query params: {query_params}")

        # ROUTE 1: GET / → Health check
        if path == "/" and not any(query_params):
            logger.info("Health check request")
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(
                    {
                        "status": "healthy",
                        "api": "Steam Games API",
                        "version": "1.0",
                        "endpoints": {
                            "health": "/?",
                            "games_by_year": "/?year=2023",
                            "games_by_genre": "/?genre=Action",
                            "top_games": "/?top=true",
                        },
                    }
                ),
            }

        # ROUTE 2: GET /?year=XXXX → Juegos por año
        if "year" in query_params:
            year_str = query_params["year"]

            try:
                year = int(year_str)
            except:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(
                        {
                            "error": 'Parámetro "year" debe ser número',
                            "example": "/?year=2023",
                        }
                    ),
                }

            logger.info(f"Buscando juegos del año {year}")

            response = table.scan(
                FilterExpression="#year = :year",
                ExpressionAttributeNames={"#year": "year"},
                ExpressionAttributeValues={":year": year},
            )

            items = response.get("Items", [])
            logger.info(f"Encontrados {len(items)} juegos")

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(
                    {"year": year, "count": len(items), "games": items},
                    default=decimal_default,
                ),
            }

        # ROUTE 3: GET /?genre=XXXX → Juegos por género
        if "genre" in query_params:
            genre = query_params["genre"]

            logger.info(f"Buscando juegos del género {genre}")

            response = table.scan(
                FilterExpression="contains(#genre, :genre)",
                ExpressionAttributeNames={"#genre": "genre"},
                ExpressionAttributeValues={":genre": genre},
            )

            items = response.get("Items", [])
            logger.info(f"Encontrados {len(items)} juegos")

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(
                    {"genre": genre, "count": len(items), "games": items},
                    default=decimal_default,
                ),
            }

        # ROUTE 4: GET /?top=true → Top 10 juegos más caros
        if "top" in query_params:
            logger.info("Buscando top 10 juegos")

            response = table.scan(Limit=100)

            # Ordenar por precio descendente
            items = sorted(
                response.get("Items", []),
                key=lambda x: float(x.get("price", 0)),
                reverse=True,
            )[:10]

            logger.info(f"Retornando {len(items)} juegos")

            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps(
                    {"count": len(items), "top_games": items}, default=decimal_default
                ),
            }

        # Si no hay parámetros, retornar ayuda
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "error": "Parámetro requerido",
                    "usage": {
                        "health": "/?",
                        "by_year": "/?year=2023",
                        "by_genre": "/?genre=Action",
                        "top_10": "/?top=true",
                    },
                }
            ),
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
