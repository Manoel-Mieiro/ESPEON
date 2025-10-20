from dotenv import load_dotenv
from app import create_app
import os

load_dotenv(".env")

APP_ENV = os.getenv("APP_ENV", "DEV").upper()

app = create_app()

if __name__ == "__main__":
    if APP_ENV == "PRD":
        PORT = int(os.environ.get("PORT", 5000))
        HOST = "0.0.0.0"
        DEBUG = False
    else:
        PORT = int(os.getenv("FLASK_RUN_PORT", 5000))
        HOST = "127.0.0.1"
        DEBUG = True

    print(f"Starting server in {APP_ENV} mode on {HOST}:{PORT}")
    app.run(debug=DEBUG, host=HOST, port=PORT)
