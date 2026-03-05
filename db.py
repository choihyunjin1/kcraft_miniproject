from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# mongodb connection (local or external via env variable)
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.dbjungle
# app.logger.info(client.list_database_names()) # check the connection