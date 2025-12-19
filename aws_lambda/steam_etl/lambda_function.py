import json
import boto3
import pandas as pd
from datetime import datetime
from decimal import Decimal
import logging
import os

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB resource
# Note: In a real Lambda environment, we rely on IAM roles.
# Locally, you need AWS credentials configured.
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("steam_games")


def lambda_handler(event, context):
    """
    ETL Pipeline ejecutado en Lambda
    - Extract: Lee CSV del mismo package
    - Transform: Limpia y normaliza datos
    - Load: Carga a DynamoDB
    """

    try:
        logger.info("=" * 50)
        logger.info("INICIANDO STEAM GAMES ETL PIPELINE")
        logger.info("=" * 50)

        # 1. EXTRACT: Cargar datos del CSV
        csv_path = os.path.join(os.path.dirname(__file__), "steam_games.csv")
        logger.info(f"📥 EXTRACT: Leyendo CSV desde {csv_path}...")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Archivo {csv_path} no encontrado.")

        df = pd.read_csv(csv_path)
        original_count = len(df)
        logger.info(f"   ✓ Registros cargados: {original_count}")

        # 2. TRANSFORM: Limpieza y normalización
        logger.info("🔄 TRANSFORM: Limpiando datos...")

        # Adaptación de esquema (Mapeo de columnas CSV a esquema DynamoDB esperado)
        # CSV headers: publisher,genres,title,release_date,discount_price,specs,price,early_access,id,sentiment,metascore,release_year

        # Renombrar 'genres' a 'genre' si es necesario
        if "genres" in df.columns and "genre" not in df.columns:
            df.rename(columns={"genres": "genre"}, inplace=True)

        # Crear columnas faltantes con valores por defecto
        if "developer" not in df.columns:
            df["developer"] = "Unknown"  # CSV no tiene developer, usamos placeholder

        if "platform" not in df.columns:
            df["platform"] = "PC"  # Asumimos PC por defecto

        if "genre" not in df.columns:
            df["genre"] = "Unknown"

        # Eliminar filas con valores críticos NULL
        # Nota: 'id' es crítico para DynamoDB (Partition Key)
        critical_cols = ["id", "title", "release_year"]
        # Verificar que existan
        existing_critical = [c for c in critical_cols if c in df.columns]
        df = df.dropna(subset=existing_critical)

        logger.info(f"   ✓ Registros después de limpieza: {len(df)}")

        # Normalizar tipos de datos
        df["id"] = (
            df["id"].astype(str).str.replace(".0", "", regex=False)
        )  # Quitar decimales si se leyó como float
        df["release_year"] = (
            pd.to_numeric(df["release_year"], errors="coerce").fillna(0).astype(int)
        )
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

        # Crear timestamp
        df["processed_at"] = datetime.now().isoformat()

        # Rellenar valores NULL en columnas opcionales
        df = df.fillna(
            {
                "genre": "Unknown",
                "developer": "Unknown",
                "publisher": "Unknown",
                "platform": "PC",
            }
        )

        logger.info("   ✓ Datos normalizados")

        # 3. LOAD: Insertar en DynamoDB
        logger.info("📤 LOAD: Cargando a DynamoDB...")

        # Usar batch_writer para optimizar writes
        # overwrite_by_pkeys parameter helps avoid duplicates if logic allows,
        # though standard batch_writer acts as put (overwrite).
        with table.batch_writer(overwrite_by_pkeys=["game_id"]) as batch:
            success_count = 0
            error_count = 0

            for _, row in df.iterrows():
                try:
                    # Preparar item
                    # Convertir float a Decimal para DynamoDB
                    price_val = Decimal(str(row["price"]))

                    item = {
                        "game_id": str(row["id"]),
                        "title": str(row["title"]),
                        "genre": str(row["genre"]),
                        "developer": str(row["developer"]),
                        "publisher": str(row["publisher"]),
                        "platform": str(row["platform"]),
                        "price": price_val,
                        "year": int(row["release_year"]),
                        "processed_at": row["processed_at"],
                    }

                    # Insertar
                    batch.put_item(Item=item)
                    success_count += 1

                except Exception as e:
                    logger.error(
                        f"Error procesando juego {row.get('id', 'unknown')}: {str(e)}"
                    )
                    error_count += 1
                    continue

        logger.info(f"   ✓ Registros insertados: {success_count}")
        logger.info(f"   ⚠️  Registros con error: {error_count}")

        # Respuesta exitosa
        response = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "ETL Pipeline completado exitosamente",
                    "timestamp": datetime.now().isoformat(),
                    "metrics": {
                        "original_records": original_count,
                        "processed_records": success_count,
                        "failed_records": error_count,
                        "success_rate": (
                            f"{(success_count/original_count)*100:.2f}%"
                            if original_count > 0
                            else "0%"
                        ),
                    },
                }
            ),
        }

        logger.info("=" * 50)
        logger.info("✅ PIPELINE COMPLETADO")
        logger.info("=" * 50)

        return response

    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": str(e), "timestamp": datetime.now().isoformat()}
            ),
        }


if __name__ == "__main__":
    # Test local
    print("Ejecutando prueba local...")
    # Mockear evento y contexto
    print(lambda_handler({}, {}))
