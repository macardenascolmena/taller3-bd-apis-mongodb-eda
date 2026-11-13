"""
ingesta.py - Taller 3 (Bases de Datos para Ciencia de Datos)

Extrae cervecerías desde la API pública Open Brewery DB
(https://api.openbrewerydb.org) y las guarda CRUDAS (sin modificar)
en MongoDB:  base de datos `taller3_db`  ->  colección `raw_data`.
"""

import os
import sys
import time

import requests
from pymongo import MongoClient, ReplaceOne
from pymongo.errors import PyMongoError

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_URL = "https://api.openbrewerydb.org/v1/breweries"
PER_PAGE = 200
MIN_RECORDS = 100
TARGET_RECORDS = 400
MAX_RETRIES = 3

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "taller3_db"
COLLECTION_NAME = "raw_data"


def fetch_page(page: int) -> list[dict]:
    params = {"per_page": PER_PAGE, "page": page}
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(API_URL, params=params, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            print(f"  [!] Error en página {page} (intento {attempt}/{MAX_RETRIES}): {exc}")
            time.sleep(2 * attempt)
    raise RuntimeError(f"No se pudo descargar la página {page} tras {MAX_RETRIES} intentos.")


def extract() -> list[dict]:
    records: list[dict] = []
    page = 1
    while len(records) < TARGET_RECORDS:
        data = fetch_page(page)
        if not data:
            break
        records.extend(data)
        print(f"Página {page}: {len(data)} registros (acumulado: {len(records)})")
        page += 1
        time.sleep(0.5)
    return records[:TARGET_RECORDS]


def load(records: list[dict]) -> None:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
    client.admin.command("ping")
    collection = client[DB_NAME][COLLECTION_NAME]

    operations = []
    for rec in records:
        doc = dict(rec)
        doc["_id"] = rec["id"]
        operations.append(ReplaceOne({"_id": doc["_id"]}, doc, upsert=True))

    result = collection.bulk_write(operations, ordered=False)
    print(f"Insertados nuevos: {result.upserted_count} | "
          f"Ya existentes (reemplazados idénticos): {result.matched_count}")
    print(f"Total documentos en {DB_NAME}.{COLLECTION_NAME}: "
          f"{collection.count_documents({})}")
    client.close()
    
    
def main() -> None:
    print("== Extracción desde Open Brewery DB ==")
    records = extract()
    if len(records) < MIN_RECORDS:
        sys.exit(f"Solo se descargaron {len(records)} registros (< {MIN_RECORDS}).")
    print(f"Total descargado: {len(records)} registros\n")

    print("== Carga en MongoDB ==")
    try:
        load(records)
    except PyMongoError as exc:
        sys.exit(f"Error con MongoDB: {exc}")
    print("Ingesta finalizada correctamente.")


if __name__ == "__main__":
    main()    