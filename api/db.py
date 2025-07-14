import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env")

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)


def seedMongo():
    with open("db.json", "r") as f:
        data = json.load(f)
    for db_item in data:
        db_name = db_item["database"]
        collection_names = db_item["collections"]

        db = client[db_name]
        existing_collections = db.list_collection_names()

        for c in collection_names:
            if c in existing_collections:
                print(f"[{db_name}] Collection '{c}' já existe.")
            else:
                try:
                    db.create_collection(c)
                    print(f"[{db_name}] Collection '{c}' criada com sucesso.")
                except Exception as e:
                    print(f"[{db_name}] Erro ao criar a collection '{c}': {e}")
