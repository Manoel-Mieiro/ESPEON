import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import psycopg2

load_dotenv(".env")
APP_ENV = os.getenv("APP_ENV", "DEV")

if APP_ENV.upper() == "PRD":
    # Ambiente PRD
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não definida no ambiente de produção!")

    result = urlparse(DATABASE_URL)
    POSTGRES_USER = result.username
    POSTGRES_PASSWORD = result.password
    POSTGRES_HOST = result.hostname
    POSTGRES_PORT = result.port
    POSTGRES_DB = result.path.lstrip('/')
else:
    # Ambiente DEV
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


# Conexão
try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    print(f"Conectado ao PostgreSQL com sucesso! ({APP_ENV})")
except Exception as e:
    print(f"Erro ao conectar ao banco ({APP_ENV}): {e}")
