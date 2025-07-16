from dotenv import load_dotenv
from db import seedMongo
from app import create_app
import os

load_dotenv(".env")

PORT = int(os.getenv("FLASK_RUN_PORT", 5000))

print(f"Port loaded from .env: {PORT}")

app = create_app()

if __name__ == "__main__":
    print("Server started at port", PORT)
    print("Executando seed...\n", seedMongo())
    app.run(debug=False, port=PORT)
