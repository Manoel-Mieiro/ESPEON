import { MongoClient } from "mongodb";
import dotenv from "dotenv";
dotenv.config();

const uri = process.env.DB_URI || "mongodb://localhost:27017";
const client = new MongoClient(uri);

let db;

async function ConnectToDatabase() {
  if (!db) {
    try {
      await client.connect();
      db = client.db(process.env.DB_NAME);
      console.log("Connected to database:", process.env.DB_NAME);
    } catch (error) {
      console.error("Connection failed", error);
    }
  }
  return db;
}

function GetDb() {
  if (!db) {
    throw new Error("MongoDB not connected. Call connectToDatabase first.");
  }
  return db;
}

export default { ConnectToDatabase, GetDb };
