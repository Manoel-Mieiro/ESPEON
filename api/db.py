import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")

APP_ENV = os.getenv("APP_ENV", "DEV").upper()

if APP_ENV == "PRD":
    MONGO_URI = os.getenv("MONGO_URI_ATLAS")
    if not MONGO_URI:
        raise ValueError(
            "MONGO_URI_ATLAS não definida no ambiente de produção!")
else:
    MONGO_URI = os.getenv("MONGO_URI_LOCAL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)

print(f"Conectado ao MongoDB ({APP_ENV})")
